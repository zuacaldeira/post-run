"""Turning calendar entries into something the app can read.

The interesting part is `exercises()`. Stryd writes its drill and stretch
sessions as prose with the demo links inline:

    - lunge matrix (engage the glutes):
       - Front Step Lunge: https://www.youtube.com/watch?v=Pl2W1NosCog

which means the cards do not have to be transcribed by hand -- and transcribing
them by hand is not safe. Read off a screenshot, two of those ids came out
wrong: the front step lunge takes a lowercase L, and the back step lunge carries
two capital I's. Both plausible alternatives are live 404s. Parsing the link
removes the eye from the loop entirely.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

VIDEO = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?(?:[^\s]*&)?v=|youtu\.be/)([A-Za-z0-9_-]{11})"
)
# a leading bullet, and the punctuation a label trails off with
BULLET = re.compile(r"^[\s\-\u2022\.,]*")
TRAIL = re.compile(r"[\s:\-]+$")
# labels that name nothing: the line was only there to introduce a link
EMPTY_LABEL = re.compile(r"^(video|videos|e\.?g\.?|link|links|and)?$", re.I)


def _clean(text: str) -> str:
    return TRAIL.sub("", BULLET.sub("", text)).strip()


# A dose is a count with a unit: reps, lunges, seconds, metres. Stryd states it
# in the line that introduces a group of links rather than beside each one --
# "Perform 3 lunges each leg of the following exercises", then three links on the
# next line; "5 reps each leg", then two; "2 x 15 - 20 meters for each of three
# drills", then three.
DOSE = re.compile(
    r"\b(\d+\s*(?:x|×)\s*\d+(?:\s*[-\u2013]\s*\d+)?\s*(?:m\b|meters?|metres?)"
    r"|\d+(?:\s*[-\u2013]\s*|\s+to\s+)?\d*\s*(?:reps?|lunges|seconds?|secs?|s)\b"
    r"|\d+\s*(?:m\b|meters?|metres?)"
    r"|\d+(?=\s+each\s+(?:leg|side)\b))"
    r"(\s+(?:each|per)\s+(?:leg|side|arm|way|direction)s?)?", re.I)


# A line that introduces a *group*, not one that happens to end in a colon.
# "…of the following exercises", "…for each of three drills:". A bare colon is
# not enough: in the stretch list every item ends with one before its link.
INTRODUCER = re.compile(r"\bfollowing\b|\beach of\b", re.I)
# An introducer that states two doses cannot be applied to either. "Start with
# 30 seconds each for the hip stretching, and 3 to five reps of each of the
# other exercises" governs two groups, and taking the first number gave the
# glute thrusts the hip stretch's 30 seconds.
TWO_DOSES = re.compile(r"\band\b[^.]*\b(reps?|seconds?|minutes?|met(?:er|re)s?|"
                       r"two|three|four|five|six|eight|ten)\b", re.I)


def dose_near(lines: list[str], i: int, back: int = 3) -> str:
    """The dose governing the link on line `i`.

    Its own line first. Failing that, the line that introduced the group it
    belongs to, within three lines -- Stryd states a count once and then lists
    the links under it: "Perform 3 lunges each leg of the following exercises".

    The walk stops the moment it crosses a line carrying a dose of its own,
    because that dose belongs to a different exercise. Without that, the hip
    flexor in the stretch list inherits the glute stretch's 30s from the line
    above it, and a card confidently states a number the plan never gave it.

    The cost is a dose occasionally left unread -- the fence drills' five reps
    each leg sit in a bullet that introduces nothing. Those say "as prescribed",
    with the prescription folded into the group directly above them. Silence is
    the acceptable failure here; a wrong number is not.
    """
    own = DOSE.search(lines[i])
    if own:
        return re.sub(r"\s+", " ", own.group(0)).strip()

    for j in range(i - 1, max(-1, i - back) - 1, -1):
        line = lines[j]
        if not line.strip():
            continue
        m = DOSE.search(line)
        if m and INTRODUCER.search(line) and not TWO_DOSES.search(line):
            return re.sub(r"\s+", " ", m.group(0)).strip()
        if m:
            return ""          # a neighbour's dose; ours is simply not stated
    return ""


def exercises(desc: str) -> list[dict]:
    """Every demo link in a prescription, with the label that introduces it.

    A label sits either before the link on its own line, or on the line above
    when the link was put on a line of its own. Anything that resolves to no
    label at all keeps the video and says so, rather than being dropped: a
    nameless card is fixable, a missing one is invisible.
    """
    lines = (desc or "").split("\n")
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for i, line in enumerate(lines):
        # Where the previous link on this line ended. Stryd puts three lunges on
        # one line -- "Front Step Lunge: <url>, Back Step Lunge: <url>, ..." --
        # and taking everything before the match would label every one of them
        # after the first "Front Step Lunge: https".
        cursor = 0
        for m in VIDEO.finditer(line):
            label = _clean(line[cursor:m.start()])
            cursor = m.end()
            # Where this exercise is described. Usually the link's own line, but
            # Stryd often puts the label on one line and the URL on the next --
            # and that label line is this exercise's, not a neighbour's, which
            # is where its dose is written.
            own = i
            if EMPTY_LABEL.match(label):
                for back in range(i - 1, -1, -1):
                    if lines[back].strip():
                        candidate = _clean(lines[back])
                        if not EMPTY_LABEL.match(candidate):
                            label = candidate
                            own = back
                        break
            key = (label.lower(), m.group(1))
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "label": label,
                "id": m.group(1),
                "line": line.strip(),
                "dose": dose_near(lines, own),
            })
    return out


def verify(items: list[dict], *, timeout: int = 12) -> list[dict]:
    """Ask YouTube whether each id is real, public and embeddable.

    Once, at sync time, rather than never. An id that 404s here would be a card
    that silently shows nothing on a phone, in a bathroom, mid-routine.
    """
    for item in items:
        url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(
            {"url": "https://www.youtube.com/watch?v=" + item["id"], "format": "json"}
        )
        try:
            with urllib.request.urlopen(url, timeout=timeout) as res:
                meta = json.loads(res.read().decode("utf-8"))
            item["ok"] = True
            item["video_title"] = meta.get("title", "")
            item["channel"] = meta.get("author_name", "")
        except urllib.error.HTTPError as exc:
            # 401 is Stryd-side embedding disabled; 404 is gone or private
            item["ok"] = False
            item["error"] = "HTTP {}".format(exc.code)
        except Exception as exc:                            # network, timeout, bad JSON
            item["ok"] = False
            item["error"] = exc.__class__.__name__
    return items


def _digest(title: str, desc: str) -> str:
    """A short stable name for one session's text, so days can point at it."""
    return hashlib.sha256((title + "\x00" + desc).encode("utf-8")).hexdigest()[:12]


PRE = re.compile(r"\bpre[\s\-_]*run\b", re.I)
POST = re.compile(r"\bpost[\s\-_]*run\b", re.I)


def when(entry: dict) -> str | None:
    """Whether a session belongs before or after the run.

    The payload says so outright: a supplemental carries
    `exercise.recommended_timing`, "pre-run" or "post-run". The text search
    behind it is the fallback for a row that has no such field, not the
    primary -- guessing from prose when the data states it would be perverse.
    """
    for hay in (entry.get("timing", ""), entry.get("kind", ""),
                entry.get("title", ""), entry.get("desc", "")[:200]):
        if PRE.search(hay or ""):
            return "pre"
        if POST.search(hay or ""):
            return "post"
    return None


def build(entries: list[dict], *, since: str | None = None, do_verify: bool = False,
          token_expires_at: str | None = None) -> dict:
    """The document the app reads."""
    from .calendar import is_run

    days: dict[str, dict] = {}
    defs: dict[str, dict] = {}
    for e in entries:
        if since and e["day"] < since:
            continue
        day = days.setdefault(e["day"], {"run": None, "sessions": []})
        if is_run(e):
            day["run"] = {
                "title": e["title"],
                "desc": e["desc"],
                "duration_s": e["duration_s"],
                "distance_m": e["distance_m"],
                "rss": e["rss"],
                "zones": e["zones"],
            }
        else:
            # A row with a date but neither a title nor a description is not a
            # session -- `plans` carries the block's own start and end dates and
            # matches every other test for a calendar entry.
            if not (e["title"] or e["desc"]):
                continue
            # The same five sessions are prescribed every day of a block, so the
            # text is stored once and referenced. Written out per day it came to
            # 228 KB for 39 days, against an app of 138 KB -- for one routine
            # repeated verbatim.
            key = _digest(e["title"], e["desc"])
            if key not in defs:
                items = exercises(e["desc"])
                if do_verify:
                    verify(items)
                defs[key] = {
                    "collection": e["collection"],
                    "kind": e["kind"],
                    "when": when(e),
                    "title": e["title"],
                    "desc": e["desc"],
                    "exercises": items,
                }
            if key not in day["sessions"]:
                day["sessions"].append(key)

    return {
        "source": "stryd",
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        # When the credential behind this data stops working. These tokens last
        # hours, not months, so the app can say the sync is about to go stale
        # before it does rather than after -- an expiry is a warning, a stale
        # plan is only ever a symptom.
        "token_expires_at": token_expires_at,
        "sessions": defs,
        "days": dict(sorted(days.items())),
    }
