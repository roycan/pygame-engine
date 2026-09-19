"""RogueEdu game engine package.

Sub-packages:
    actions       -- intent-based Action types returned by entities.
    base_classes  -- GameObject / Character / Hero / Villain / NPC / Wall blueprints.
    view          -- SafeGameView, the read-only world snapshot given to entities.
    core          -- GameEngine: authoritative turn loop, validation, turn JSON.

Students subclass the blueprints from base_classes; they never mutate the
world directly. Every intent flows back to the engine as an Action object.
"""
