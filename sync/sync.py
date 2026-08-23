#!/usr/bin/env python3
"""
Hourly: ask intervals.icu what was planned and what was actually run, and drop a
small JSON file where the app can read it.

intervals.icu is the single source on purpose. Garmin has no usable API (see
deploy/README.md), but the watch already syncs to intervals.icu carrying the
Stryd power with it, and the plan lives there too -- so one call answers both
halves of "was this executed", instead of reconciling two services that
disagree about what a day is.

    INTERVALS_ATHLETE_ID=i123456 INTERVALS_API_KEY=... python3 sync.py --once

Env:
    INTERVALS_ATHLETE_ID, INTERVALS_API_KEY   required
    OUT             where to write        (default /data/training.json)
    SYNC_INTERVAL   seconds between runs  (default 3600)
    SYNC_DAYS       days of history       (default 30)
"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request
from datetime import date, datetime, timedelta, timezone

API = "https://intervals.icu/api/v1"


def get(path, athlete, key, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{API}/athlete/{athlete}/{path}" + (f"?{q}" if q else "")
    req = urllib.request.Request(url, headers={
        "Authorization": "Basic " + base64.b64encode(f"API_KEY:{key}".encode()).decode(),
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())


def pick(d, *names, default=None):
    """intervals.icu returns a wide row and field names vary by endpoint; take the
    first one that is actually present rather than guessing a single spelling."""
    for n in names:
        v = d.get(n)
        if v not in (None, ""):
            return v
    return default


def day_of(d, *names):
    v = pick(d, *names)
    return v[:10] if isinstance(v, str) else None


def normalise(events, activities, days_back):
    today = date.today()
    span = {(today - timedelta(days=i)).isoformat() for i in range(days_back)}
    span |= {(today + timedelta(days=i)).isoformat() for i in range(8)}   # the week ahead
    out = {d: {"planned": [], "done": []} for d in sorted(span)}

    for e in events or []:
        if str(pick(e, "category", default="")).upper() != "WORKOUT":
            continue
        d = day_of(e, "start_date_local", "start_date", "date")
        if d not in out:
            continue
        secs = pick(e, "moving_time", "icu_training_load_time", default=0) or 0
        out[d]["planned"].append({
            "name": pick(e, "name", default="Workout"),
            "type": pick(e, "type", "category", default="Run"),
            "minutes": round(secs / 60) or None,
        })

    for a in activities or []:
        d = day_of(a, "start_date_local", "start_date")
        if d not in out:
            continue
        metres = pick(a, "distance", "icu_distance", default=0) or 0
        secs = pick(a, "moving_time", "elapsed_time", default=0) or 0
        out[d]["done"].append({
            "name": pick(a, "name", default="Activity"),
            "type": pick(a, "type", "sport", default="Activity"),
            "km": round(metres / 1000, 1) if metres else None,
            "minutes": round(secs / 60) or None,
            "watts": pick(a, "icu_average_watts", "average_watts", "icu_weighted_avg_watts"),
            "hr": pick(a, "average_heartrate", "icu_average_hr"),
        })

    for d, v in out.items():
        planned, done, past = bool(v["planned"]), bool(v["done"]), d < today.isoformat()
        # A planned day with nothing on it is only "missed" once the day is over;
        # until then it is still ahead of you.
        v["state"] = ("done"      if planned and done
                      else "unplanned" if done
                      else ("missed" if past else "planned") if planned
                      else "rest")
    return out


def build(athlete, key, days_back, dump=None):
    today = date.today()
    oldest = (today - timedelta(days=days_back)).isoformat()
    newest = (today + timedelta(days=7)).isoformat()
    events = get("events", athlete, key, oldest=oldest, newest=newest)
    acts = get("activities", athlete, key, oldest=oldest, newest=newest)
    if dump:
        for name, blob in (("events", events), ("activities", acts)):
            p = os.path.join(dump, f"{name}.json")
            with open(p, "w") as f:
                json.dump(blob, f, indent=2)
            print(f"wrote {p} ({len(blob or [])} rows)", file=sys.stderr)
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "days": normalise(events, acts, days_back),
    }


def write(payload, out):
    """Write beside the target and rename, so a reader never catches a half file."""
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, separators=(",", ":"))
    os.replace(tmp, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="one pass, then exit")
    ap.add_argument("--out", default=os.environ.get("OUT", "/data/training.json"))
    ap.add_argument("--days", type=int, default=int(os.environ.get("SYNC_DAYS", "30")))
    ap.add_argument("--dump", metavar="DIR", help="also save the raw API responses")
    a = ap.parse_args()

    athlete = os.environ.get("INTERVALS_ATHLETE_ID")
    key = os.environ.get("INTERVALS_API_KEY")
    if not athlete or not key:
        sys.exit("set INTERVALS_ATHLETE_ID and INTERVALS_API_KEY")

    interval = int(os.environ.get("SYNC_INTERVAL", "3600"))
    while True:
        try:
            payload = build(athlete, key, a.days, a.dump)
            write(payload, a.out)
            n = sum(len(d["done"]) for d in payload["days"].values())
            print(f"{payload['generated']}  {n} activities across {len(payload['days'])} days"
                  f" -> {a.out}", flush=True)
        except urllib.error.HTTPError as e:
            # Never overwrite good data with a failure: the app keeps showing the
            # last successful sync rather than going blank because of one 500.
            print(f"HTTP {e.code}: {e.read()[:200]!r}", file=sys.stderr, flush=True)
        except Exception as e:                                   # noqa: BLE001
            print(f"sync failed: {e!r}", file=sys.stderr, flush=True)
        if a.once:
            return
        time.sleep(interval)


if __name__ == "__main__":
    main()
