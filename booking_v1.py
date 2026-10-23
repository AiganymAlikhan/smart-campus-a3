"""Room availability checker."""

DAY_MINUTES = 1440
MAX_DURATION = 120


def _is_int(value):
    """True for real integers; rejects bool (an int subclass) and floats."""
    return isinstance(value, int) and not isinstance(value, bool)


def can_book(start, end, now, blocked, existing):
    """Return True if the interval [start, end) can be booked.

    start, end, now: integer minutes after midnight (now assumed valid, 0-1439).
    blocked: truthy if the room is blocked.
    existing: list of (start, end) tuples; read only, never mutated.
    """
    # AC3: a blocked room rejects every request.
    if blocked:
        return False

    # AC1: integer times within the day, start before end, start after now.
    if not (_is_int(start) and _is_int(end)):
        return False
    if not (0 <= start < end <= DAY_MINUTES):
        return False
    if start <= now:
        return False

    # AC2: at most 120 minutes (exactly 120 allowed).
    if end - start > MAX_DURATION:
        return False

    # AC4: no overlap; touching endpoints are allowed.
    for ex_start, ex_end in existing:
        if start < ex_end and ex_start < end:
            return False

    # AC5: valid request.
    return True
