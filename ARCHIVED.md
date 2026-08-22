# Archived — Postrun is part of Fundo

Retired 22 August 2026. The live app was `postrun.zuacaldeira.com`; that origin
now serves a tombstone that unregisters the installed app's service worker and
leaves for Fundo.

## What moved, and where it lives now

| What | Now |
|---|---|
| Reading the drills, mobility and strength out of the plan | `Fundo/src/fundo/ingest/powercenter.py` — `planned_sessions()` |
| Parsing movements and demo links out of the prescription | same file — `exercises()` |
| Where they are kept | `planned_session` in `canonical.sqlite` |
| Running a session hands-free | `Fundo/src/fundo/ui/session.py`, served at `/{token}/session` |
| The 21 pictograms | same file |

The single most valuable thing carried across is a comment, not code:
`deleted` is authoritative for PowerCenter's `workouts` and **not** for its
`supplementals`, where every row of the live block is flagged and the app goes
on showing them. Honouring the flag there drops the entire supplemental plan.
That is `DELETED_IS_AUTHORITATIVE` in Fundo, with a test named after it.

## What did not move, deliberately

- **chroma.js and the runtime contrast solver.** Fundo's looks are authored and
  fixed; a solver would be machinery with nothing to solve.
- **Bluetooth device reading.** Fundo has far richer device data through FIT and
  Garmin ingest. Live pairing is its own feature, not part of a merge.
- **The progressive plank dial** — the earned 5s bump, gated on 14 days and six
  sessions. Nothing in Fundo replaces it yet, and a movement whose dose the plan
  does not state currently falls back to the queue's default. This is the one
  real capability that was lost rather than relocated.
- **The desktop "Block" view** (`web/index.html`). Fundo's own plan and trends
  screens cover it.

## The two design records

`DESIGN.md` and `PRODUCT.md` describe the app as it stood at the end, which is
the Munich '72 build at commit `832c333`, not the final one. The last visual
pass replaced that world and was never re-documented — `a0fc978` is the app that
actually shipped. Read the commits, not the design record, for the last word.
