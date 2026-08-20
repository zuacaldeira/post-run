"""Reading the calendar payload without assuming its shape.

fundo reads `payload["workouts"]` and builds its plan from that. It is not
wrong, but it is partial: that collection holds the *runs*. The Drill and
Stretch entries a Stryd calendar shows on the same day live somewhere else in
the payload, and reading only the one collection is how a plan that plainly
contains pre- and post-run work looked like it contained none.

So nothing here names a collection up front. It walks the payload, takes every
list of objects that look like calendar entries, and remembers which key each
came from. A collection nobody anticipated shows up as data rather than as
silence.
"""

from __future__ import annotations

import re
from typing import Any, Iterator

DATE_KEYS = ("date", "day", "scheduled_date", "start_date", "timestamp")
TITLE_KEYS = ("title", "name", "label")
DESC_KEYS = ("desc", "description", "notes", "text", "body")
# fields that only a run carries; their absence is what separates a drill from a session
RUN_KEYS = ("duration", "distance", "stress", "intensity_zones", "blocks")
TYPE_KEYS = ("type", "category", "kind", "workout_type", "activity_type", "subtype")

ISO_DAY = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def _first(d: dict, keys) -> Any:
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None


def _day_of(d: dict) -> str | None:
    raw = _first(d, DATE_KEYS)
    if raw is None:
        return None
    m = ISO_DAY.match(str(raw))
    return m.group(1) if m else None


def looks_like_entry(d: Any) -> bool:
    return isinstance(d, dict) and _day_of(d) is not None


def collections(payload: dict) -> list[dict]:
    """What is in here, for a first look. Discovery output, not a data path."""
    out = []
    for key, value in sorted(payload.items()):
        if not isinstance(value, list) or not value:
            continue
        objs = [v for v in value if isinstance(v, dict)]
        if not objs:
            continue
        keys: set[str] = set()
        for o in objs[:50]:
            keys |= set(o.keys())
        out.append({
            "collection": key,
            "rows": len(value),
            "entries": sum(1 for o in objs if looks_like_entry(o)),
            "fields": sorted(keys),
        })
    return out


def harvest(payload: dict) -> Iterator[dict]:
    """Every calendar entry in the payload, whatever collection it sat in.

    `deleted` is honoured here rather than downstream. PowerCenter keeps the
    rows of superseded plans alongside the live one, so taking everything would
    put two contradictory sessions on the same day.
    """
    for key, value in payload.items():
        if not isinstance(value, list):
            continue
        for raw in value:
            if not looks_like_entry(raw):
                continue
            if raw.get("deleted"):
                continue
            inner = raw.get("workout") if isinstance(raw.get("workout"), dict) else {}
            yield {
                "collection": key,
                "day": _day_of(raw),
                "title": str(_first(inner, TITLE_KEYS) or _first(raw, TITLE_KEYS) or "").strip(),
                "desc": str(_first(inner, DESC_KEYS) or _first(raw, DESC_KEYS) or "").strip(),
                "kind": str(_first(raw, TYPE_KEYS) or _first(inner, TYPE_KEYS) or "").strip(),
                "duration_s": raw.get("duration"),
                "distance_m": raw.get("distance"),
                "rss": raw.get("stress"),
                "zones": raw.get("intensity_zones") or [],
                "raw_keys": sorted(raw.keys()),
            }


def is_run(entry: dict) -> bool:
    """A run has a length and a load. A drill or a stretch is a list of things to do."""
    return any(entry.get(k) for k in ("duration_s", "distance_m", "rss"))
