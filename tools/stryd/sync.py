"""Fetch the plan, write plan.json. The whole job.

    python3 -m tools.stryd.sync --discover        # what is in the payload
    python3 -m tools.stryd.sync --dry-run         # what would be written
    python3 -m tools.stryd.sync                   # write it

Run it weekly at most. The calendar route hands back the entire history in one
response, so polling buys nothing and costs someone else's bandwidth.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import calendar as cal
from . import client, token, transform

DEFAULT_OUT = Path("/var/www/postrun.zuacaldeira.com/plan.json")


def _payload(args) -> dict:
    """The calendar, and as a side effect the token's expiry for the document."""
    if args.payload:                       # a saved response, for working offline
        try:
            return json.loads(Path(args.payload).read_text(encoding="utf-8"))
        except OSError as exc:
            raise client.ApiError("cannot read {}: {}".format(args.payload, exc.strerror)) from None
        except json.JSONDecodeError as exc:
            raise client.ApiError("{} is not JSON: {}".format(args.payload, exc.msg)) from None

    tok = token.read(Path(args.token) if args.token else None)
    if token.is_expired(tok):
        when = token.expires_at(tok)
        raise SystemExit(
            "The token expired at {}. Copy a fresh one from local storage.\n\n{}".format(
                when.isoformat() if when else "an unknown time",
                token.HOW_TO_GET_ONE.format(path=args.token or token.DEFAULT_PATH),
            )
        )
    when = token.expires_at(tok)
    _payload.token_expires_at = when.isoformat() if when else None
    data = client.calendar(tok, token.athlete_id(tok))
    if args.save_payload:
        Path(args.save_payload).write_text(json.dumps(data), encoding="utf-8")
    return data


def _write(path: Path, doc: dict) -> None:
    """Atomically, or not at all.

    A half-written file is worse here than a stale one: the app caches what it
    is served, so a truncated plan.json would be kept and re-served offline.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    os.chmod(tmp, 0o644)
    os.replace(tmp, path)


def _check(args) -> int:
    """Is there a usable token, and how long is it good for.

    Prints where it came from, when it expires and which athlete it addresses --
    never the token, and never enough of it to reconstruct one. It makes no
    request, so it says nothing about whether Stryd would accept it; an
    unexpired token can still have been revoked.
    """
    print("looking in:", token.source())
    try:
        tok = token.read(Path(args.token) if args.token else None)
    except token.MissingToken as exc:
        print(exc, file=sys.stderr)
        return 2

    print("found     : {} characters, {} segments".format(len(tok), len(tok.split("."))))
    if len(tok.split(".")) != 3:
        print("This does not look like a JWT. A partial paste is the usual cause.",
              file=sys.stderr)
        return 2

    try:
        print("athlete   :", token.athlete_id(tok))
    except token.MissingToken as exc:
        print("athlete   : unknown --", exc, file=sys.stderr)
        return 2

    when = token.expires_at(tok)
    if when is None:
        print("expires   : no exp claim; only the API can say")
        return 0

    from datetime import datetime, timezone
    left = when - datetime.now(timezone.utc)
    if left.total_seconds() <= 0:
        print("expires   : {}  EXPIRED".format(when.isoformat()), file=sys.stderr)
        return 2
    days, rem = divmod(int(left.total_seconds()), 86400)
    print("expires   : {}  ({}d {}h left)".format(when.isoformat(), days, rem // 3600))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sync the Stryd plan into plan.json")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="where plan.json goes")
    ap.add_argument("--since", help="drop days before this ISO date")
    ap.add_argument("--verify", action="store_true",
                    help="check every demo link against YouTube's oembed")
    ap.add_argument("--check", action="store_true",
                    help="report where the token came from and when it expires, and stop")
    ap.add_argument("--discover", action="store_true",
                    help="print the payload's collections and fields, write nothing")
    ap.add_argument("--dry-run", action="store_true", help="summarise, write nothing")
    ap.add_argument("--token", help="path to the token file")
    ap.add_argument("--payload", help="read a saved payload instead of fetching")
    ap.add_argument("--save-payload", help="keep the raw response here")
    args = ap.parse_args(argv)

    if args.check:
        return _check(args)

    try:
        payload = _payload(args)
    except (token.MissingToken, client.ApiError) as exc:
        # Say what went wrong and leave whatever is on disk alone. A failed sync
        # must never be the reason yesterday's plan disappears.
        print(exc, file=sys.stderr)
        return 2

    if args.discover:
        print("top-level keys:", ", ".join(sorted(payload.keys())) or "(none)")
        for c in cal.collections(payload):
            print("\n{}  rows={} calendar-like={}".format(
                c["collection"], c["rows"], c["entries"]))
            print("  fields: " + ", ".join(c["fields"]))
        return 0

    entries = list(cal.harvest(payload))
    runs = [e for e in entries if cal.is_run(e)]
    others = [e for e in entries if not cal.is_run(e)]
    print("entries: {}  runs: {}  sessions: {}".format(len(entries), len(runs), len(others)))
    by_collection: dict[str, int] = {}
    for e in others:
        by_collection[e["collection"]] = by_collection.get(e["collection"], 0) + 1
    if by_collection:
        print("non-run entries by collection: " + ", ".join(
            "{}={}".format(k, v) for k, v in sorted(by_collection.items())))
    else:
        print("no non-run entries found -- if the calendar shows drills, they are in a "
              "collection this did not recognise. Run --discover.")

    doc = transform.build(entries, since=args.since, do_verify=args.verify,
                          token_expires_at=getattr(_payload, "token_expires_at", None))

    if args.verify:
        # sessions are stored once and referenced by day, so check them once too
        bad = [(sess["title"], x)
               for sess in doc["sessions"].values()
               for x in sess["exercises"] if not x.get("ok")]
        for title, x in bad:
            print("  BAD LINK {!r} {} {}".format(title, x["id"], x.get("error", "")),
                  file=sys.stderr)
        print("demo links checked; {} unusable".format(len(bad)))

    if args.dry_run:
        print(json.dumps(doc, ensure_ascii=False, indent=2)[:4000])
        return 0

    _write(Path(args.out), doc)
    print("wrote {} ({} days)".format(args.out, len(doc["days"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
