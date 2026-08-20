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
BULLET = re.compile(r"^[\s\-\u2022\.]*")
TRAIL = re.compile(r"[\s:\-]+$")
# labels that name nothing: the line was only there to introduce a link
EMPTY_LABEL = re.compile(r"^(video|videos|e\.?g\.?|link|links|and)?$", re.I)


def _clean(text: str) -> str:
    return TRAIL.sub("", BULLET.sub("", text)).strip()


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
        for m in VIDEO.finditer(line):
            label = _clean(line[: m.start()])
            if EMPTY_LABEL.match(label):
                for back in range(i - 1, -1, -1):
                    if lines[back].strip():
                        candidate = _clean(lines[back])
                        if not EMPTY_LABEL.match(candidate):
                            label = candidate
                        break
            key = (label.lower(), m.group(1))
            if key in seen:
                continue
            seen.add(key)
            out.append({"label": label, "id": m.group(1), "line": line.strip()})
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


PRE = re.compile(r"\bpre[\s\-_]*run\b", re.I)
POST = re.compile(r"\bpost[\s\-_]*run\b", re.I)


def when(entry: dict) -> str | None:
    """Whether a session belongs before or after the run.

    Stryd's own app labels them "Pre Run" and "Post Run". Which field carries
    that is not known until a real payload has been seen, so this reads the
    fields that might and falls back to the text, rather than guessing one.
    """
    for hay in (entry.get("kind", ""), entry.get("title", ""), entry.get("desc", "")[:200]):
        if PRE.search(hay or ""):
            return "pre"
        if POST.search(hay or ""):
            return "post"
    return None


def build(entries: list[dict], *, since: str | None = None, do_verify: bool = False) -> dict:
    """The document the app reads."""
    from .calendar import is_run

    days: dict[str, dict] = {}
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
            items = exercises(e["desc"])
            if do_verify:
                verify(items)
            day["sessions"].append({
                "collection": e["collection"],
                "kind": e["kind"],
                "when": when(e),
                "title": e["title"],
                "desc": e["desc"],
                "exercises": items,
            })

    return {
        "source": "stryd",
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "days": dict(sorted(days.items())),
    }
