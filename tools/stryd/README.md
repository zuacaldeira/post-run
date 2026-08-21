# Syncing the Stryd plan

Pulls the training plan out of PowerCenter and writes `plan.json` next to the
app. The app reads it same-origin and falls back to the copy baked into
`index.html` when it is absent, stale-free, or unreachable.

```sh
python3 -m tools.stryd.sync --discover     # what the payload contains
python3 -m tools.stryd.sync --dry-run      # what would be written
python3 -m tools.stryd.sync --verify       # write it, checking every demo link
```

`--since` defaults to `today` and is resolved when it runs, not when it is
written -- a date baked into a unit file is stale the day after. `--since all`
keeps the whole history, which is 866 days and 340 KB against an app of 138 KB;
from today it is 39 days and 38 KB. The past belongs to fundo, not to a phone in
a bathroom.

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

### The short way

From the repo, on a machine that can reach the server:

```sh
./token <jwt>        # or ./token  to be prompted, or ./token -c  from the clipboard
```

It writes the token, waits for the path unit to fire the sync, and reports back:
who the token is for, how long it lasts, whether the sync ran, and what
plan.json now holds.

`./token -b` prints a bookmarklet. Clicked on stryd.com while signed in, it
finds the JWT among whatever keys Stryd is using and copies it, so the whole
refresh is a click and `./token -c` -- no DevTools, no paste, and the token
never reaches a shell history.

What is deliberately *not* automated is the sign-in and the reading of the token
by anything that would carry it somewhere else. A credential is worth the two
seconds it costs to move by hand.

Check what you placed without printing it:

```sh
python3 -m tools.stryd.sync --check
```

It reports where the token came from, how long it is good for and which athlete
it addresses -- never the token. It makes no request, so an unexpired token that
has been revoked still looks fine to it.

### Three ways in, in this order

1. **A systemd credential.** Under `LoadCredential=`, pid 1 reads the file as
   root before dropping to the service user and leaves the contents on a ramfs
   only that unit can read. The token stays `root:root 0600` and the service
   user never gets access to the file -- which matters here, because the sync
   runs as `www-data` and so does nginx. Nothing lands in the environment, and
   the directory is unmounted when the unit stops.
2. **`STRYD_TOKEN`** in the environment.
3. **The file** at `STRYD_TOKEN_FILE`, default `/etc/postrun/stryd.token`.

The last two exist because neither is available under systemd and both are how
this gets run by hand: `--discover` and `--dry-run` happen from a shell, where
there is no manager to hand anything over.

**`LoadCredential=` requires the source file to exist**, and fails the unit with
an opaque `243/CREDENTIALS` if it does not. So the file is created empty and
root-owned at install time; the sync then reports the missing token in its own
words, in the journal, and writes nothing.

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

## When it runs

**On paste, not on a clock.** A PowerCenter token lasts hours -- the first real
one here had twelve left -- so a weekly timer would nearly always fire on an
expired credential, and a shorter interval would only fail more often. The
moment worth syncing is the moment there is a fresh token, which is exactly when
the token file changes.

`deploy/postrun-stryd-sync.path` watches it and starts the service:

```sh
install -m644 deploy/postrun-stryd-sync.{service,path} /etc/systemd/system/
install -m755 deploy/place-stryd-token.sh /usr/local/sbin/place-stryd-token
systemctl daemon-reload && systemctl enable --now postrun-stryd-sync.path
```

Then re-authenticating is the whole workflow:

```sh
place-stryd-token          # paste the JWT, Enter, Ctrl-D
```

It writes the file atomically and the sync fires by itself. Atomically matters:
a plain `cat > file` truncates first, so the path unit would fire once on an
empty file and again on the real one.

`deploy/postrun-stryd-sync.timer` is kept but left **disabled**. It is there for
a future with a credential that outlives the day; against session tokens it is
noise.

The service runs as `www-data` with write access to the web root and nothing
else -- not even to the token, which reaches it as a systemd credential.

## This is a private API

There is no published documentation, no developer programme and no terms saying
what is allowed. The endpoints came from a working client, not a spec. It can
change or vanish without notice, which is why every call fails loudly rather
than papering over a shape it did not expect — and why the plan stays baked into
`index.html` as a floor. The sync is what picks up a *future* block; it is not
what keeps the app working.
