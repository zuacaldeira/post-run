# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Today: one hand-written `index.html` (~178 KB, no framework, no npm, no build step)
plus `sw.js`, served as static files by nginx behind TLS, installable as a PWA. A
second surface, `web/index.html`, is a separate static page. Python (`tools/stryd/`)
runs server-side and writes `plan.json` next to the app.

**The stack is explicitly an open question for the next phase.** The user has put the
single-file, no-build constraint and the strict CSP on the table rather than treating
them as permanent, because the data ambition below may not fit inside them. Nothing has
been decided; the current shape holds until it is. Whoever reopens it should read the
"It used to be a container" note in `deploy/README.md` first — this project has already
removed one layer of machinery it did not need.

## Users

One user: the owner, a runner following a Stryd training plan. This is a personal tool,
not a product for strangers. There is no sign-up, no second account, no onboarding for
someone who has never seen it, and no requirement to generalise beyond one athlete's
routine, devices and Stryd account. Design decisions may optimise for him specifically.

The real usage scene is the constraint that matters: a phone, held or propped, one hand,
often sweaty, immediately after a run — and, for the pre-run part, before leaving the
house. A desktop browser is the second scene, used to look at a block of training rather
than to execute a session.

## Product Purpose

Show the training day whole, in one place, and make it executable.

Stryd prescribes three things that live in three different places: pre-run drills, the
run itself, and post-run core and mobility. Following them otherwise means an app, a
screenshot and a memory. Post-Run pulls the real prescription out of PowerCenter and
renders the day as one continuous thing — pre-run, run, post-run — with hold timers,
sound cues, vibration, an autopilot that runs the session without being touched, and
demonstration videos on the cards.

Success is a session completed correctly without the phone being picked up mid-exercise,
and a day where nothing prescribed was missed because it was somewhere else.

## Positioning

**The day, whole, in one place.** A generic interval timer can count seconds; it cannot
know that today's plan has a lunge matrix before the run and side planks after it. The
mechanism is that the cards are read out of the prescription itself — `transform.exercises()`
parses Stryd's prose and pulls the label and YouTube id straight out of the text, so an
exercise card is never transcribed by eye. (Transcription was tried and produced two
plausible-looking video ids that were live 404s, which is why `--verify` exists.)

## Operating Context

- **The day has three phases**: pre-run drills, the run prescription, post-run core &
  mobility — plus optional contrast-bath recovery, deliberately outside the session.
- **Where the plan comes from**: `tools/stryd/sync.py` reads PowerCenter's private API
  server-side and writes `plan.json` into the web root. The app fetches it same-origin.
- **When it syncs**: on token paste, not on a clock. A PowerCenter JWT lasts hours, so a
  systemd `.path` unit watches the token file and fires the sync the moment it changes.
  `./token` places one; `./token -b` prints a bookmarklet that copies the JWT off
  stryd.com. The timer unit exists but is deliberately disabled.
- **The token is moved by hand, always.** Password-to-JWT exchange is deliberately not
  implemented, because it would mean handling a plaintext password.
- **Deployment is `./deploy.sh`** — rsync to `/var/www/postrun.zuacaldeira.com`. No
  container, no registry, no CI. The nginx vhost is in the repo because the headers *are*
  the deployment: `no-cache` everywhere, the CSP, and an explicit
  `application/manifest+json`.
- **Devices**: a Stryd pod (read over Running Speed & Cadence plus Cycling Power — there
  is no BLE service for running power) and any standard heart-rate strap, both paired
  from the settings panel. Chrome on Android can do this; Safari on iOS cannot, and the
  app says so rather than showing a button that does nothing.

## Capabilities and Constraints

Confirmed and working:

- Three-phase day built from `plan.json`, with a baked-in plan in `index.html` as the
  floor when the sync is absent, stale or unreachable.
- Autopilot: hold timers, sound cues, vibration, `navigator.wakeLock`, a spotlight on the
  exercise being performed, and a progress ring overlay.
- A progressive front-plank dial (5s steps) with an earned-bump rule: 14 days *and* 6
  logged sessions, capped at 120s — past which progress comes from variation, not duration.
- Swipe between days; the day is in the URL.
- Live BLE readings from pod and strap during a session.
- A local completion log in `localStorage` (`postrun.v1`), capped at 600 entries.
- Offline via service worker; the whole routine is cached, only the YouTube demos need a
  connection.
- A desktop surface, `web/index.html` — "The Block" — drawing a training block as load
  and power per day.

Hard constraints, confirmed:

- **Offline-first and phone-first.** The routine must work cached with no connection,
  one-handed, mid-session.
- **The Stryd plan is authority; the baked copy is the floor.** Never fabricate a
  session. A failed sync leaves the previous `plan.json` untouched and exits non-zero — a
  stale plan is worth far more than no plan, because the app caches what it is served.
- **The Stryd API is private and undocumented.** No published spec, no developer
  programme, no terms. It can change or vanish. Every call must fail loudly rather than
  paper over an unexpected shape, and no collection is named up front — `calendar.harvest()`
  walks the payload and reports what it finds, which is how the drill and stretch entries
  were discovered in the first place. `deleted` rows are honoured.
- **The token never reaches the browser and never reaches a shell history.**

Constraints now explicitly open, not confirmed:

- The single-file / no-build-step shape.
- The `self` + YouTube CSP.

Undecided:

- Whether device history is stored on the server, and in what form.
- Whether "The Block" desktop surface stays a separate page or becomes part of the app.
- The APK path described in `README.md` §B refers to a `PostRunRoutine` folder that is
  not in this repository. Treat native Android as not currently part of the product.

## Open Direction: gadgets, history, interpretation

Stated by the user during init and recorded as direction, not as a shipped capability:

> connect to all my gadgets and have detailed information collected and analyzed

This is a real expansion beyond what exists. Today the app reads two devices *live*
during a session and keeps only a small local record of which cards were completed.
The stated ambition is **persisted and interpreted**: device streams and sessions kept
as history alongside the Stryd sync, so that weeks of what actually happened accumulate —
and then something reads that history back and forms an opinion. Trends, flags, whether
the prescription is landing. Not just a chart.

Consequences to hold in mind, none of them decided:

- Persistence beyond `localStorage` implies storage on the server that already runs the
  sync — which is what puts the stack question above on the table.
- "All my gadgets" is currently two (pod, strap) and is unenumerated beyond that. What
  else exists should be established before designing for it.
- Interpretation means the product starts making claims about the user's training. Those
  claims must be traceable to recorded data, never invented, on the same principle that
  governs the plan.

## Brand Commitments

- Name: **Post-Run** / "Post-Run Core & Mobility". Live at `postrun.zuacaldeira.com`.
- Icons: `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`.
- Backdrop photograph: Pierre-Antoine FRANCK on Unsplash (`bg.jpg`), Unsplash License.
  Attribution is not required but is kept in `README.md` on purpose.
- Voice, evident across the code comments, both READMEs and every commit subject: plain,
  declarative, lower-case commit lines that say what changed in the user's own terms
  ("Stop claiming a run the day does not have"). It explains *why* a decision was made,
  names the trade honestly, and admits what was got wrong. It never sells. Copy in the
  app is written the same way — the recovery note argues both sides of the cold bath
  rather than recommending it. This is a real commitment and future copy must match it.

## Evidence on Hand

- Real training data via the live Stryd sync; a real plan baked into `index.html`.
- Real, `--verify`-checked YouTube demonstration ids on the exercise cards.
- A working deployment, TLS, and systemd units, all documented in `deploy/README.md`.
- **No** testimonials, users, benchmarks, pricing, press, or third-party validation —
  and there should not be, since there is one user. Do not fabricate any.

## Product Principles

1. **The day is one thing.** Pre-run, run, post-run belong on one surface in one order.
   Anything that splits them back apart is a regression.
2. **Executable beats informative.** The measure is whether a session can be completed
   without touching the phone, not whether the screen is comprehensive.
3. **Never invent a session, and never invent a conclusion.** Real prescription or the
   baked floor; recorded data or silence. Fail loudly rather than paper over a shape.
4. **The credential moves by hand.** Convenience never justifies holding a password or
   carrying a token somewhere it does not need to go.
5. **Say why, and say what it costs.** Every explanation in this project names the trade
   instead of recommending. Keep it that way.

## Accessibility & Inclusion

No externally required standard, but the incumbent code takes it seriously and that
should be preserved: `prefers-reduced-motion`, `prefers-reduced-transparency` and
`forced-colors` all drop the moving backdrop; contrast is solved against the scrim rather
than guessed (`web/index.html` documents raising a caption grey from 2.58:1 to 4.59:1);
`:focus-visible` is styled everywhere; iOS is told plainly that Web Bluetooth is
unavailable instead of being shown a dead button. The usage scene — sweaty hands, a
propped phone, motion — makes large touch targets and high contrast functional
requirements, not preferences.
