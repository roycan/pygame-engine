"""GameEngine: the authoritative simulation core.

The engine owns EVERYTHING:

* loud validation at construction (win conditions, goal position),
* registration of entities (draining their stat-clamp warnings into the
  setup log),
* the turn lifecycle with early-exit win checks and the Dead-Actor rule,
* villain turn resolution in registration order with tile reservation,
* damage sanitization (the engine NEVER trusts student-computed damage),
* and emission of the turn JSON payload consumed by the browser.

Design invariants (see plans/prompt_v2.md for the full contract):

* Dead villains are RETAINED in ``self.villains`` with ``is_alive() ==
  False`` forever. Purging them would permanently break the
  ``clear_and_reach_goal`` win condition. They are merely hidden from
  ``board_state`` and ignored by collision logic.
* ``AttackAction`` carries a direction, never a damage number. Damage is
  read from the attacker's ``calculate_attack_damage()`` and sanitized
  (negative -> 0, above MAX_ATK -> MAX_ATK) with loud warning events.
* The turn can end early: a win check runs immediately after every hero
  action, and the hero's death aborts the remaining villain turns.
"""

from __future__ import annotations

import difflib

from .actions import Action, AttackAction, MoveAction, SpeakAction, WaitAction
from .base_classes import MAX_ATK, Hero, NPC, Villain, Wall
from .view import SafeGameView

#: The three supported win conditions (validated LOUDLY in __init__).
WIN_CONDITIONS = ("defeat_all", "reach_goal", "clear_and_reach_goal")
_GOAL_MODES = ("reach_goal", "clear_and_reach_goal")

#: Player key -> cardinal (dx, dy). Bump-to-attack and bump-to-talk fall
#: out of the same table: what happens depends on WHO occupies the tile.
KEY_DIRS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}


class GameEngine:
    """The rulebook, the referee and the scoreboard, in one object."""

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        win_condition: str = "defeat_all",
        goal_pos: tuple[int, int] | None = None,
    ):
        # ---- Loud validation of the game configuration -----------------
        if win_condition not in WIN_CONDITIONS:
            close = difflib.get_close_matches(str(win_condition), WIN_CONDITIONS, n=1)
            hint = f" Did you mean '{close[0]}'?" if close else ""
            raise ValueError(
                f"Unknown win_condition {win_condition!r}.{hint} "
                f"Valid options: {', '.join(WIN_CONDITIONS)}."
            )
        if win_condition in _GOAL_MODES and goal_pos is None:
            raise ValueError(
                f"win_condition {win_condition!r} requires a goal_pos=(x, y)."
            )
        self.width = width
        self.height = height
        self.win_condition = win_condition
        self.goal_pos = tuple(goal_pos) if goal_pos is not None else None
        if self.goal_pos is not None:
            gx, gy = self.goal_pos
            if not (0 <= gx < self.width and 0 <= gy < self.height):
                raise ValueError(
                    f"goal_pos {self.goal_pos} is outside the "
                    f"{self.width}x{self.height} board."
                )

        # ---- World state ------------------------------------------------
        self.hero: Hero | None = None
        self.villains: list[Villain] = []  # registration order = turn order
        self.npcs: list[NPC] = []
        self.walls: list[Wall] = []

        self.turn_count = 0
        self.game_over = False
        self.won = False
        self.active_dialogue: str | None = None

        self.logs: list[str] = []  # setup log + beginner-friendly turn log
        self.events: list[dict] = []  # raw event dicts for the CURRENT turn

    @property
    def _hero(self) -> Hero:
        """The registered hero, or a LOUD RuntimeError if ``create_game()``
        forgot one. Internal engine code uses this instead of the raw
        ``self.hero`` attribute, so a missing hero produces a clear,
        student-friendly error instead of a confusing None crash.
        """
        if self.hero is None:
            raise RuntimeError(
                "No hero has been registered. Call add_hero(...) inside "
                "create_game() before playing."
            )
        return self.hero

    # ------------------------------------------------------------------
    # Registration API (used by student_starter/game_config.py)
    # ------------------------------------------------------------------

    def add_hero(self, hero: Hero) -> None:
        """Register THE hero. Exactly one per game; duplicates raise."""
        if not isinstance(hero, Hero):
            raise TypeError(f"add_hero expects a Hero subclass, got {type(hero).__name__}.")
        if self.hero is not None:
            raise ValueError("This game already has a hero. Only one is allowed.")
        self._check_bounds(hero.x, hero.y, hero.name)
        self._check_unoccupied(hero.x, hero.y, hero.name)
        self._drain_warnings(hero)
        self.hero = hero

    def add_villain(self, villain: Villain) -> None:
        """Register a villain. Registration order defines turn order."""
        if not isinstance(villain, Villain):
            raise TypeError(
                f"add_villain expects a Villain subclass, got {type(villain).__name__}."
            )
        self._check_bounds(villain.x, villain.y, villain.name)
        self._check_unoccupied(villain.x, villain.y, villain.name)
        villain._death_logged = False  # corpse log fires once, on first skip
        self._drain_warnings(villain)
        self.villains.append(villain)

    def add_npc(self, npc: NPC) -> None:
        """Register an NPC (a friendly, indestructible talker)."""
        if not isinstance(npc, NPC):
            raise TypeError(f"add_npc expects an NPC subclass, got {type(npc).__name__}.")
        self._check_bounds(npc.x, npc.y, npc.name)
        self._check_unoccupied(npc.x, npc.y, npc.name)
        self._drain_warnings(npc)
        self.npcs.append(npc)

    def add_wall(self, wall: Wall) -> None:
        """Register a wall. A wall may never sit on the goal tile."""
        if not isinstance(wall, Wall):
            raise TypeError(f"add_wall expects a Wall, got {type(wall).__name__}.")
        self._check_bounds(wall.x, wall.y, wall.name)
        self._check_unoccupied(wall.x, wall.y, wall.name)
        if self.goal_pos is not None and wall.position == self.goal_pos:
            raise ValueError(
                f"Wall at {wall.position} sits on the goal tile {self.goal_pos}. "
                f"The game would be unwinnable."
            )
        self.walls.append(wall)

    def _drain_warnings(self, obj) -> None:
        """Move a character's construction-time clamp warnings into the
        setup log, so no clamp is ever silent (loud-invariant doctrine)."""
        for warning in getattr(obj, "warnings", []):
            self.logs.append(f"[SETUP WARNING] {obj.name}: {warning}")
        if hasattr(obj, "warnings"):
            obj.warnings.clear()

    def _check_bounds(self, x: int, y: int, name: str) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"{name} is placed at ({x}, {y}), outside the "
                f"{self.width}x{self.height} board."
            )

    def _check_unoccupied(self, x: int, y: int, name: str) -> None:
        if self._tile_occupied(x, y):
            raise ValueError(f"{name} is placed on an already occupied tile ({x}, {y}).")

    def _tile_occupied(self, x: int, y: int) -> bool:
        if self.hero is not None and self.hero.position == (x, y):
            return True
        if any(v.position == (x, y) for v in self.villains):
            return True
        if any(n.position == (x, y) for n in self.npcs):
            return True
        return any(w.position == (x, y) for w in self.walls)

    # ------------------------------------------------------------------
    # Board queries
    # ------------------------------------------------------------------

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _wall_at(self, x: int, y: int) -> bool:
        return any(w.position == (x, y) for w in self.walls)

    def _living_villain_at(self, x: int, y: int) -> Villain | None:
        for v in self.villains:
            if v.is_alive() and v.position == (x, y):
                return v
        return None

    def _npc_at(self, x: int, y: int) -> NPC | None:
        for n in self.npcs:
            if n.position == (x, y):
                return n
        return None

    def _passable_for(self, mover, x: int, y: int) -> bool:
        """Can ``mover`` stand on (x, y)? Walls, the hero, NPCs and OTHER
        living villains all block. Dead villains block nothing."""
        if not self._in_bounds(x, y) or self._wall_at(x, y):
            return False
        if self.hero is not None and self.hero.position == (x, y):
            return False
        if self._npc_at(x, y) is not None:
            return False
        for v in self.villains:
            if v is mover or not v.is_alive():
                continue
            if v.position == (x, y):
                return False
        return True

    def _build_view(self) -> SafeGameView:
        """A fresh read-only snapshot, taken at the moment it is handed out."""
        return SafeGameView(self)

    # ------------------------------------------------------------------
    # Win condition
    # ------------------------------------------------------------------

    def check_win_condition(self) -> bool:
        """Evaluate the configured win condition.

        The ``len(self.villains) > 0`` guard prevents a turn-zero win on
        a villain-less map in ``defeat_all`` mode. Dead villains are
        RETAINED in the list (never purged), so this check stays correct
        for the whole game -- that is what keeps ``clear_and_reach_goal``
        winnable after the last villain falls.
        """
        all_villains_dead = len(self.villains) > 0 and all(
            not v.is_alive() for v in self.villains
        )
        at_goal = (
            self.goal_pos is not None
            and self.hero is not None
            and self.hero.position == self.goal_pos
        )
        if self.win_condition == "defeat_all":
            return all_villains_dead
        if self.win_condition == "reach_goal":
            return at_goal
        if self.win_condition == "clear_and_reach_goal":
            return all_villains_dead and at_goal
        raise ValueError(f"Unknown win_condition {self.win_condition!r}.")  # loud

    def _goal_locked(self) -> bool:
        """In clear_and_reach mode the goal renders locked until all
        villains are down."""
        return self.win_condition == "clear_and_reach_goal" and any(
            v.is_alive() for v in self.villains
        )

    # ------------------------------------------------------------------
    # Events and damage (the loud-invariants machinery)
    # ------------------------------------------------------------------

    def _event(self, beginner_text: str, actor: str, action: str, result: str,
               tile_pos) -> None:
        """Record one event (detailed dict + beginner-friendly log line)."""
        self.events.append(
            {
                "beginner_text": beginner_text,
                "actor": actor,
                "action": action,
                "result": result,
                "tile_pos": list(tile_pos) if tile_pos is not None else None,
            }
        )
        self.logs.append(beginner_text)

    def _sanitized_damage(self, attacker) -> int:
        """Read damage from the attacker, sanitizing LOUDLY.

        Student overrides of calculate_attack_damage() are allowed for
        flavor but never trusted: negative -> 0 (no heal exploits), and
        anything above MAX_ATK is capped. Every sanitization emits a
        WARNING event naming the actor and the offending value.
        """
        raw = attacker.calculate_attack_damage()
        if raw < 0:
            self._event(
                f"CHEAT GUARD: {attacker.name} tried to deal {raw} damage "
                f"(negative). Sanitized to 0.",
                attacker.name, "DamageSanitize", "WARNING",
                [attacker.x, attacker.y],
            )
            return 0
        if raw > MAX_ATK:
            self._event(
                f"CHEAT GUARD: {attacker.name} tried to deal {raw} damage "
                f"(above MAX_ATK={MAX_ATK}). Sanitized to {MAX_ATK}.",
                attacker.name, "DamageSanitize", "WARNING",
                [attacker.x, attacker.y],
            )
            return MAX_ATK
        return raw

    def _validated_action(self, actor, action) -> Action:
        """Return a legal action, converting illegal input loudly.

        * Not an Action at all (or None) -> WARNING + WaitAction.
        * Diagonal / oversized vector -> WARNING + WaitAction
          (movement is strictly cardinal).
        """
        if not isinstance(action, Action):
            self._event(
                f"{actor.name} returned {action!r}, which is not an Action. "
                f"Treated as a wait.",
                actor.name, "InvalidAction", "WARNING", [actor.x, actor.y],
            )
            return WaitAction()
        if isinstance(action, (MoveAction, AttackAction)):
            if abs(action.dx) + abs(action.dy) != 1:
                self._event(
                    f"{actor.name} tried an illegal step "
                    f"({action.dx}, {action.dy}). Movement is cardinal only "
                    f"(N/S/E/W). Converted to a wait.",
                    actor.name, type(action).__name__, "WARNING",
                    [actor.x, actor.y],
                )
                return WaitAction()
        return action

    # ------------------------------------------------------------------
    # The turn lifecycle
    # ------------------------------------------------------------------

    def step(self, key: str) -> dict:
        """Advance the game by one player input; return the turn payload.

        Lifecycle (see plans/prompt_v2.md §5):
          0. frozen if game_over
          1. dialogue pause frame: any key dismisses, no turn advances
          2. hero input: space=wait, WASD bump-to-attack / bump-to-talk /
             blocked / move
          3. early-exit win check after every hero action
          4. villain phase (unless the hero bumped an NPC -- dialogue
             freezes villains for that tick)
          5. hero death aborts remaining villains
        """
        if self.game_over:
            return self.payload()

        self.events = []

        # 1. Dialogue pause frame: dismissing costs nothing.
        if self.active_dialogue is not None:
            self.active_dialogue = None
            self._event(
                "Dialogue closed. The villains held their breath -- nothing moved.",
                self._hero.name, "CloseDialogue", "INFO", [self._hero.x, self._hero.y],
            )
            return self.payload()

        # 2. Hero input.
        if key == "space":
            self._event(
                f"{self._hero.name} waits and watches.",
                self._hero.name, "WaitAction", "SUCCESS", [self._hero.x, self._hero.y],
            )
            self.turn_count += 1
            self._after_hero_action()

        elif key in KEY_DIRS:
            dx, dy = KEY_DIRS[key]
            tx, ty = self._hero.x + dx, self._hero.y + dy
            target_villain = self._living_villain_at(tx, ty)
            bumped_npc = self._npc_at(tx, ty)

            if target_villain is not None:
                # Bump-to-attack: the hero stays put and strikes.
                self._hero_attacks(target_villain)
                self.turn_count += 1
                self._after_hero_action()
            elif bumped_npc is not None:
                # Bump-to-talk: dialogue opens, villains freeze this tick.
                spoken = bumped_npc.interact(self._build_view())
                if not isinstance(spoken, SpeakAction):
                    self._event(
                        f"{bumped_npc.name}.interact() returned "
                        f"{type(spoken).__name__} instead of a SpeakAction; "
                        f"showing it as raw text.",
                        bumped_npc.name, "SpeakAction", "WARNING", [tx, ty],
                    )
                    message = str(spoken)
                else:
                    message = spoken.message
                self.active_dialogue = message
                self.turn_count += 1
                self._event(
                    f"{bumped_npc.name} says: {message}",
                    bumped_npc.name, "SpeakAction", "SUCCESS", [tx, ty],
                )
                # Deliberately NO villain phase: dialogue freezes enemies.
            elif not self._in_bounds(tx, ty) or self._wall_at(tx, ty):
                self._event(
                    f"BLOCKED: {self._hero.name} bumped into a wall. "
                    f"Nothing moved; no turn was spent.",
                    self._hero.name, "MoveAction", "BLOCKED", [tx, ty],
                )
                # A blocked bump spends no turn: the world is unchanged.
            else:
                self._hero.x, self._hero.y = tx, ty
                self.turn_count += 1
                self._event(
                    f"{self._hero.name} moves to ({tx}, {ty}).",
                    self._hero.name, "MoveAction", "SUCCESS", [tx, ty],
                )
                self._after_hero_action()

        else:
            self._event(
                f"Ignored key {key!r}. Use w/a/s/d to move, space to wait.",
                "Game", "IgnoreInput", "INFO", None,
            )

        return self.payload()

    def _after_hero_action(self) -> None:
        """Early-exit win check, then the villain phase (unless won)."""
        if self.check_win_condition():
            self.won = True
            self.game_over = True
            self._event(
                f"🏆 VICTORY! {self._hero.name} fulfilled the objective "
                f"on turn {self.turn_count}. The villains never got to respond.",
                self._hero.name, "WinCheck", "SUCCESS", [self._hero.x, self._hero.y],
            )
            return
        self._villain_phase()

    def _hero_attacks(self, villain: Villain) -> None:
        """The hero strikes an adjacent villain (bump-to-attack)."""
        damage = self._sanitized_damage(self._hero)
        applied = villain.take_damage(damage)
        self._event(
            f"{self._hero.name} strikes {villain.name} for {applied} damage! "
            f"({villain.name}: {villain.hp}/{villain.max_hp} hp left)",
            self._hero.name, "AttackAction", "SUCCESS", [villain.x, villain.y],
        )
        if not villain.is_alive():
            self._event(
                f"{villain.name} is defeated!",
                self._hero.name, "AttackAction", "INFO", [villain.x, villain.y],
            )

    # ------------------------------------------------------------------
    # Villain phase
    # ------------------------------------------------------------------

    def _villain_phase(self) -> None:
        """Living villains act in registration order.

        ``reserved_tiles`` implements same-tick contention: the first
        villain to claim a destination wins; later villains targeting it
        are BLOCKED at their origin. The set is discarded afterwards.
        """
        reserved: set[tuple[int, int]] = set()

        for villain in self.villains:
            if self.game_over:
                break  # hero died mid-phase: remaining villains abort

            # Dead-Actor rule: corpses skip their turn, logged exactly once.
            if not villain.is_alive():
                if not villain._death_logged:
                    self._event(
                        f"{villain.name} is defeated and cannot act.",
                        villain.name, "SkipTurn", "INFO", [villain.x, villain.y],
                    )
                    villain._death_logged = True
                continue

            view = self._build_view()
            action = self._validated_action(villain, villain.act(view))

            if isinstance(action, WaitAction):
                self._event(
                    f"{villain.name} waits.",
                    villain.name, "WaitAction", "SUCCESS", [villain.x, villain.y],
                )
            elif isinstance(action, MoveAction):
                self._villain_moves(villain, action, reserved)
            elif isinstance(action, AttackAction):
                self._villain_attacks(villain, action)
            else:
                self._event(
                    f"{villain.name} returned an unsupported action "
                    f"({type(action).__name__}). Treated as a wait.",
                    villain.name, type(action).__name__, "WARNING",
                    [villain.x, villain.y],
                )

            # Hero death aborts the remaining villain turns immediately.
            if not self._hero.is_alive():
                self.game_over = True
                self.won = False
                self._event(
                    f"☠ {self._hero.name} has fallen. GAME OVER.",
                    self._hero.name, "HeroDefeated", "INFO",
                    [self._hero.x, self._hero.y],
                )
                break
        # Cleanup: reserved_tiles is discarded with this local variable.

    def _villain_moves(self, villain: Villain, action: MoveAction,
                       reserved: set[tuple[int, int]]) -> None:
        dest = (villain.x + action.dx, villain.y + action.dy)
        if dest in reserved:
            self._event(
                f"BLOCKED: {villain.name} tried to move into {dest}, "
                f"but another villain just claimed it. It stays put.",
                villain.name, "MoveAction", "BLOCKED", list(dest),
            )
            return
        if not self._passable_for(villain, *dest):
            self._event(
                f"BLOCKED: {villain.name} bumped into something at {dest} "
                f"and stayed at ({villain.x}, {villain.y}).",
                villain.name, "MoveAction", "BLOCKED", list(dest),
            )
            return
        reserved.add(dest)
        villain.x, villain.y = dest
        self._event(
            f"{villain.name} moves to {dest}.",
            villain.name, "MoveAction", "SUCCESS", list(dest),
        )

    def _villain_attacks(self, villain: Villain, action: AttackAction) -> None:
        """Villain directional attack: only the Hero can ever be harmed."""
        tx, ty = villain.x + action.dx, villain.y + action.dy
        if (tx, ty) == self._hero.position:
            damage = self._sanitized_damage(villain)
            applied = self._hero.take_damage(damage)
            self._event(
                f"{villain.name} hits {self._hero.name} for {applied} damage! "
                f"({self._hero.name}: {self._hero.hp}/{self._hero.max_hp} hp left)",
                villain.name, "AttackAction", "SUCCESS",
                [self._hero.x, self._hero.y],
            )
        elif self._wall_at(tx, ty):
            self._event(
                f"{villain.name} swings at a wall. Nothing happens.",
                villain.name, "AttackAction", "BLOCKED", [tx, ty],
            )
        else:
            # Empty tile or another villain: zero damage either way --
            # villains never harm each other.
            self._event(
                f"{villain.name} swings at empty air and misses.",
                villain.name, "AttackAction", "MISSED", [tx, ty],
            )

    # ------------------------------------------------------------------
    # Turn payload (the contract with the browser)
    # ------------------------------------------------------------------

    def board_state(self) -> dict:
        """The full board for rendering. Dead villains are omitted (they
        are retained internally, just not drawn)."""
        hero = self._hero
        return {
            "width": self.width,
            "height": self.height,
            "hero": {
                "name": hero.name, "x": hero.x, "y": hero.y,
                "hp": hero.hp, "max_hp": hero.max_hp, "symbol": hero.symbol(),
            },
            "villains": [
                {"name": v.name, "x": v.x, "y": v.y,
                 "hp": v.hp, "max_hp": v.max_hp, "symbol": v.symbol()}
                for v in self.villains if v.is_alive()
            ],
            "npcs": [
                {"name": n.name, "x": n.x, "y": n.y, "symbol": n.symbol()}
                for n in self.npcs
            ],
            "walls": [
                {"x": w.x, "y": w.y, "symbol": w.symbol()} for w in self.walls
            ],
        }

    def payload(self) -> dict:
        """The complete turn JSON consumed by the Flask routes and game.js.

        The required key set is frozen in tests/fixtures/turn_payload_schema.json;
        both pytest and the jsdom tests validate against that one fixture so
        the Python and JavaScript sides can never drift apart.
        """
        return {
            "turn": self.turn_count,
            "game_over": self.game_over,
            "won": self.won,
            "win_condition": self.win_condition,
            "goal_pos": list(self.goal_pos) if self.goal_pos is not None else None,
            "goal_locked": self._goal_locked(),
            "active_dialogue": self.active_dialogue,
            "board_state": self.board_state(),
            "events": self.events,
            "log": self.logs,
        }
