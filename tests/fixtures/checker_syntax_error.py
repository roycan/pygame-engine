"""Checker fixture: a syntax error (import must fail with a friendly FAIL)."""

class Oops:
    def broken(:  # <- deliberate syntax error
        pass
