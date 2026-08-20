# Syncing the Stryd plan

Pulls the training plan out of PowerCenter and writes `plan.json` next to the
app. The app reads it same-origin and falls back to the copy baked into
`index.html` when it is absent, stale-free, or unreachable.

```sh
python3 -m tools.stryd.sync --discover     # what the payload contains
python3 -m tools.stryd.sync --dry-run      # what would be written
python3 -m tools.stryd.sync --verify       # write it, checking every demo link
```

## Why this is not in the browser

The app is a static page served with `connect-src 'self'`. It cannot call
stryd.com: the CSP forbids it, Stryd sends no CORS headers for our origin, and a
credential shipped to a browser is a published credential. So the sync runs
here, holds the token, and leaves a file.

## The token

**No password ever reaches this code.** PowerCenter signs in with email and
password and returns a JWT; that exchange is deliberately not implemented,
because handling a password in plain text is a line this does not cross.

```
sign in at https://www.stryd.com
DevTools -> Application -> Local Storage -> https://www.stryd.com
copy the JWT into /etc/postrun/stryd.token
chmod 600 /etc/postrun/stryd.token
```

It expires. When it does, repeat — nothing here can renew it, and nothing here
should try, because renewing means holding the password. `sync.py` says so
plainly rather than failing with a 401.

`STRYD_TOKEN_FILE` moves the path; `STRYD_TOKEN` supplies it directly, which is
for testing rather than for a server.

## Nothing here assumes the payload's shape

fundo reads `payload["workouts"]` and builds its plan from that. It is not
wrong, but it is partial: that collection holds the **runs**. The Drill and
Stretch entries a Stryd calendar shows on the same day live somewhere else in
the payload — which is how a plan that plainly contains pre- and post-run work
looked, from the database, like it contained none.

So no collection is named up front. `calendar.harvest()` walks the payload,
takes every list of objects carrying a date, and records which key each came
from. Run `--discover` first: it prints the collections and their fields, and a
collection nobody anticipated shows up as data rather than as silence.

`deleted` is honoured. PowerCenter keeps the rows of superseded plans beside the
live one, so taking everything would put two contradictory sessions on one day.

## The cards come from the prescription

Stryd writes its sessions as prose with the demo links inline:

```
- lunge matrix (engage the glutes):
   - Front Step Lunge: https://www.youtube.com/watch?v=Pl2W1NosCog
```

`transform.exercises()` reads the label and the video id straight out of that,
so exercise cards never have to be transcribed. That matters more than it
sounds: transcribed by eye from a screenshot, two of these ids came out wrong —
the front step lunge takes a lowercase L, the back step lunge two capital I's,
and both plausible alternatives are live 404s. `--verify` then asks YouTube's
oembed whether each id is real, public and embeddable, once, at sync time. A bad
link caught here is a card that would otherwise have shown nothing on a phone,
mid-routine.

## Failure

A sync that fails leaves the previous `plan.json` alone and exits non-zero. A
stale plan is worth much more than no plan: the app caches what it is served, so
a truncated file would be kept and re-served offline. Writes go to a temp file
and are moved into place with `os.replace`, so a reader never sees half a
document.

## Scheduling

`deploy/postrun-stryd-sync.{service,timer}` run it weekly as `www-data`, with
write access to the web root and read access to the token and nothing else.

Weekly is deliberate. The calendar route returns the entire history in one
response and the plan is written once at the start of a block, so polling costs
someone else's bandwidth to learn nothing.

## This is a private API

There is no published documentation, no developer programme and no terms saying
what is allowed. The endpoints came from a working client, not a spec. It can
change or vanish without notice, which is why every call fails loudly rather
than papering over a shape it did not expect — and why the plan stays baked into
`index.html` as a floor. The sync is what picks up a *future* block; it is not
what keeps the app working.
