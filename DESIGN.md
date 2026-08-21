---
name: Post-Run
description: Two registers of one system — glass solved at runtime for executing the day, ink on paper for reading the block.
colors:
  first-light: "#F5F2FF"
  midnight-violet: "#1B1440"
  frosted-heather: "#8C86B0"
  signal-amber: "#FF8A1F"
  settled-green: "#12B981"
  settled-green-painted: "#007938"
  frosted-heather-tint: "#EFECFA"
  ink-secondary: "#2B234C"
  worst-case-backdrop: "#939199"
  glass-pane: "rgba(255,255,255,0.42)"
  chip-veil: "rgba(255,255,255,0.62)"
  session-violet: "#7B5CFF"
  stale-red: "#8A2F2F"
  letterbox-black: "#0E0A22"
  read-paper: "#E7EBF1"
  read-card: "#F6F8FB"
  read-rule: "#CBD4E0"
  read-ink: "#0F1720"
  read-ink-2: "#5A6674"
  read-ink-3: "#616A75"
  zone-easy: "#93A6BA"
  zone-steady: "#5C86AC"
  zone-tempo: "#D9A03F"
  zone-threshold: "#DC672C"
  zone-max: "#BE3624"
typography:
  display:
    fontFamily: "Antonio, system-ui, sans-serif"
    fontSize: "clamp(30px, 4vw, 46px)"
    fontWeight: 600
    lineHeight: 0.9
    letterSpacing: "0.01em"
  headline:
    fontFamily: "Antonio, system-ui, sans-serif"
    fontSize: "clamp(26px, 3vw, 38px)"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.01em"
  clock:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "clamp(34px, 10.5vw, 46px)"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "-0.04em"
    fontFeature: "tabular-nums"
  title:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "19px"
    fontWeight: 900
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "13.5px"
    fontWeight: 500
    lineHeight: 1.6
  prescription:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.72
  label:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "12px"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "0.18em"
  micro:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "10.5px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.12em"
rounded:
  none: "0"
  bar: "3px"
  key: "5px"
  badge: "15px"
  action: "16px"
  video: "20px"
  panel: "22px"
  card: "26px"
  sheet: "18px 18px 0 0"
  pill: "99px"
spacing:
  hair: "2px"
  xs: "4px"
  sm: "8px"
  gutter: "10px"
  md: "14px"
  card: "16px"
  lg: "22px"
  group: "26px"
  section: "34px"
components:
  card-exercise:
    backgroundColor: "{colors.glass-pane}"
    textColor: "{colors.midnight-violet}"
    typography: "{typography.title}"
    rounded: "{rounded.card}"
    padding: "16px"
  card-exercise-doing:
    backgroundColor: "{colors.signal-amber}"
    textColor: "{colors.midnight-violet}"
    rounded: "{rounded.card}"
    padding: "16px"
  card-exercise-done:
    backgroundColor: "{colors.settled-green-painted}"
    textColor: "#FFFFFF"
    rounded: "{rounded.card}"
    padding: "16px"
  badge:
    backgroundColor: "{colors.frosted-heather}"
    textColor: "{colors.midnight-violet}"
    rounded: "{rounded.badge}"
    height: "44px"
    width: "44px"
  button-check:
    backgroundColor: "{colors.chip-veil}"
    textColor: "{colors.midnight-violet}"
    rounded: "{rounded.pill}"
    padding: "8px 12px"
  button-hold:
    backgroundColor: "{colors.chip-veil}"
    textColor: "{colors.midnight-violet}"
    rounded: "{rounded.pill}"
    padding: "11px 17px"
  tab:
    backgroundColor: "{colors.glass-pane}"
    textColor: "{colors.midnight-violet}"
    rounded: "{rounded.pill}"
    padding: "10px 14px"
  tab-selected:
    backgroundColor: "{colors.midnight-violet}"
    textColor: "{colors.first-light}"
    rounded: "{rounded.pill}"
    padding: "10px 14px"
  panel:
    backgroundColor: "{colors.glass-pane}"
    textColor: "{colors.midnight-violet}"
    rounded: "{rounded.panel}"
    padding: "16px 17px"
  panel-read:
    backgroundColor: "{colors.read-card}"
    textColor: "{colors.read-ink}"
    rounded: "{rounded.none}"
    padding: "22px 24px"
---

# Design System: Post-Run

## Overview

**Creative North Star: "The Solved Surface"**

Nothing in the Execute register is picked by eye. The palette is a seed of five
authored colors and a set of solvers that derive every surface, rim, label and veil
from them at boot, each one proven against the worst case the backdrop can produce —
a pure black video frame under the thinnest part of the scrim. The identity of this
system is that rigour. A card is amber because a movement is being done, and it is
*that* amber because that is the lightest amber which still carries Midnight Violet at
7:1. The look is a consequence of the constraint, not a decoration applied over it.

The system runs in **two deliberate registers**, and they are allowed to look
unrelated because they answer different questions in different rooms.

- **Execute** (`index.html`) is a phone held in a wet hand immediately after a run.
  Glass panes float over a photograph, corners are generous (26px), type is heavy and
  short, and color carries exactly one meaning: what state a movement is in. Everything
  is solved at runtime.
- **Read** (`web/index.html`) is a desk and a training block seen whole. Ink on cool
  paper, zero radius, hairline rules, Antonio over IBM Plex, and color carries exactly
  one meaning: how hard the effort is. Everything is authored and static.

What binds them is method, not appearance: contrast is solved rather than guessed (the
Read register raises a caption grey from a measured 2.58:1 to 4.59:1 for exactly the
same reason the Execute register runs a solver); color means one thing at a time; and
every motion, transparency and forced-color preference is honoured rather than assumed.

**Key Characteristics:**
- Two registers, one method — glass and runtime solving to execute, ink and print to read.
- Color is a state channel, never an identity or a decoration.
- Contrast is computed against a paranoid worst case, never eyeballed.
- Depth reports state; it does not simulate height.
- Every reduced-motion, reduced-transparency and forced-colors path is a designed state, not a fallback.
- Legibility at arm's length, from the floor, mid-hold, wins every tie.

## Colors

Two palettes, one rule each: in Execute, hue means state; in Read, hue means intensity.

### Primary

- **Signal Amber** (`#FF8A1F`, painted as authored): the state of *doing*. It is the one seed
  the solver leaves alone — it already carries Midnight Violet at 7.3:1, so `fill()` exits on
  its first check. It is the highest-luminance thing on the page, carrying dark text, so the
  movement you are actually on is where the eye lands.
  It is never used decoratively, and only one element on screen can hold it at a time.
  It is also the anchor the run histogram and zone bar mix from, so a hard segment and an
  active card read as the same kind of loud.
- **Settled Green** (`#12B981` seed → `#007938` painted): the state of *done*, and the clearest
  demonstration of how this system works. The authored hex is **never painted**. `fill()`
  darkens and saturates it through 90 possible steps until white clears 5.5:1 — not 4.5:1,
  specifically so the surface sheen and the translucent veils laid over it cannot push white
  back under the threshold — and what lands on screen is a far deeper forest green at 5.54:1.
  Editing the seed changes where the solve starts, not what you see.
- **Frosted Heather** (`#8C86B0` seed → `#EFECFA` tint): the state of *todo*. Never used at
  full strength — `tintOf()` lifts it to L\*94 with chroma capped at 26 before it becomes a
  surface, so a resting card is a pale window rather than a coloured object. Nine waiting
  cards must not read as nine things. The seed itself survives only in the rim and the badge.

### Neutral

- **First Light** (`#F5F2FF`): the paper. Set on `html` alone — never on `body` as well,
  because `body`'s own background paints over a negative-z-index child and the backdrop
  photograph would never actually be seen.
- **Midnight Violet** (`#1B1440`): the ink, and the foreground on every light surface. Its
  secondary tone is not a chosen grey: `inkFor()` resolves it to `#2B234C` against the
  worst-case backdrop at 4.5:1.
- **Worst-Case Backdrop** (`#939199`): not a paintable color. It is the darkest composite
  the glass can ever sit on — pure black under a 60% scrim — and it is the background every
  contrast solve is run against. Deliberately more pessimistic than the real scrim (which
  bottoms out at 84%), so the whole palette stays valid if different footage is dropped in.
- **Glass Pane** (`rgba(255,255,255,0.42)`) and **Chip Veil** (`rgba(255,255,255,0.62)`):
  the two translucency levels. Panels and tabs take the first; pressable chips take the second.

### Tertiary

- **Session Violet** (`#7B5CFF`): the fallback anchor for charts and the solid backing for
  the session bar before the solver has run. It is the last trace of the app's original
  fixed palette and should not spread.
- **Stale Red** (`#8A2F2F`): the plan-age line when the sync has gone stale. An expired token
  is not decoration — it is the reason tomorrow's plan will not arrive — so it is the one
  place a warning color is allowed.
- **Letterbox Black** (`#0E0A22` / `#160F35`): behind YouTube frames only, so a loading
  video is a dark violet void rather than a grey rectangle.

### Read register

- **Cool Paper** (`#E7EBF1`), **Card** (`#F6F8FB`), **Rule** (`#CBD4E0`): the ground, the
  raised panel, and every hairline.
- **Print Ink** (`#0F1720`), **Ink 2** (`#5A6674`), **Ink 3** (`#616A75`): body, secondary,
  and small text. Ink 3 is the deliberate one — it carries captions, week labels, the axis
  and the eyebrows, all small, and it sits at 4.59:1 on paper rather than at the grey that
  looked right and measured 2.58:1.
- **The intensity ramp** — Easy (`#93A6BA`), Steady (`#5C86AC`), Tempo (`#D9A03F`),
  Threshold (`#DC672C`), Max (`#BE3624`): cool through hot, with only the top two zones
  allowed to be warm, so a hard day is visible from across the room and an easy week
  stays quiet.

### Named Rules

**The One Meaning Rule.** Within a register, hue answers exactly one question. In Execute
that question is "what state is this movement in"; in Read it is "how hard is this". A
color introduced to distinguish, brand, or enliven anything is a defect, not a variation.

**The Worst-Case Rule.** No foreground colour is authored. Every one is derived by solver
(`inkFor`, `fade`, `fill`) against Worst-Case Backdrop, not against the colour a surface
appears to be. Adding a hand-picked hex to a glass surface bypasses the only thing keeping
the app legible over arbitrary footage.

**The Quantised Check Rule.** Contrast is validated on the rounded 8-bit hex, never on the
float. Rounding costs about 0.01 and was landing values at 4.4999 against a 4.5 target.

## Typography

**Display Font:** Antonio 600 (Read register only, self-hosted woff2)
**Body Font:** `system-ui` stack (Execute) / IBM Plex Sans 400·600 (Read)
**Label/Mono Font:** IBM Plex Mono 400·500 (Read register)

**Character:** Execute has no typeface of its own on purpose — it uses the platform's UI
face at weight 900 with tight negative tracking, so it reads as part of the phone rather
than as a document, and it costs nothing to load offline. Read is the opposite argument:
a condensed uppercase display face against a humanist body and a mono for every figure,
because a training block is a printed thing you study, not a control you operate.

### Hierarchy

- **Display** (Antonio 600, `clamp(30px, 4vw, 46px)`, line-height .9, uppercase): the Read
  masthead, sitting on a 2px ink rule.
- **Headline** (Antonio 600, `clamp(26px, 3vw, 38px)`, line-height 1, uppercase): the
  selected day's title.
- **Clock** (900, `clamp(34px, 10.5vw, 46px)`, tracking -.04em, tabular): the session
  timer. The largest thing on the screen, always.
- **Title** (900, 19px, line-height 1.15, tracking -.02em): an exercise name on a card.
- **Body** (500, 13.5px, line-height 1.6): notes, verdicts, the prescription in Execute.
  Held to a 42ch measure where it runs long.
- **Prescription** (IBM Plex Mono 400, 12.5px, line-height 1.72): Stryd's own prose in the
  Read register. Quoted with `white-space: pre-wrap`, never restyled — it arrives with its
  own line breaks and indented lists and they are meaningful.
- **Label** (900, 12px, tracking .18em, uppercase): every section heading. `h2` and `h3`
  are visually identical by design — stepping down a level changes the outline, not the look.
- **Micro** (Plex Mono, 10.5px, tracking .12em, uppercase): axis figures, week strips,
  eyebrows, the step count.

### Named Rules

**The Floor-Read Rule.** The running clock is read from the floor, mid-hold, a couple of
feet away. It is the one element allowed to consume height, and nothing may grow past it.

**The Weight-Not-Size Rule.** Execute establishes hierarchy with weight (900 against 500)
and tracking, not with a type scale. There are only four real sizes on a card — 19, 13.5,
12, 11 — and adding a fifth flattens the three that matter.

**The Ellipsis Rule.** Single-line elements in the session bar (`what`, `phase`, `stepcount`)
truncate; they never wrap. A long exercise name must not grow the bar and push the screen
behind it out of view.

## Layout

**Execute** is a single 620px column, centred, with 16px gutters and 24px of top padding,
plus `env(safe-area-inset-bottom)` on every bottom edge. One phase is on screen at a time,
chosen from a horizontally scrolling tab strip rather than by folding four headers — a fold
answers "what else is there" by making you open things; a strip answers it at a glance. At
360px, the common narrow phone, the four tabs just miss fitting: the strip scrolls and the
type shrinks by half a step rather than being shaved until it cannot be read. While a
session runs, `body` gains `padding-bottom: calc(max(120px, 12vh) + safe-area)` so the
fixed session bar never covers the card it is timing.

Vertical rhythm is coarse and consistent: 34px between phases, 26px between groups, 16px
between cards, 10–14px inside them.

**Read** is a 1440px page with fluid `clamp(16px, 4vw, 56px)` side padding, built from a
two-column detail grid (`minmax(0,1.15fr)` against `minmax(0,1fr)`, 26px gap) and an
auto-fitting card row at `minmax(280px, 1fr)`. It collapses to one column at 900px, where
the block's own height drops from 190px to 150px.

### Named Rules

**The 620 Rule.** The Execute column never exceeds 620px, on any viewport. The flipped
card's minimum height is derived from that number (`(min(620px,100vw) - 32px) * 9/16`),
so widening the column silently breaks the video frame — and where container queries are
available the card measures itself with `100cqw` instead of trusting the constant.

**The One Phase Rule.** Exactly one phase section is displayed at a time. Two open sections
is not a denser layout, it is a lost tab strip.

## Elevation & Depth

Depth in the Execute register is a **material** — translucency, blur and saturation over a
photograph — and shadow on top of it is **a state report, not a height cue**. A card at rest
carries only a hairline inset highlight and a shadow so tight it is nearly invisible
(`-20px` spread). A card that is *being done* gains a larger, closer shadow tinted with its
own solid amber and scales to 1.015. A card that is *done* keeps a tinted green drop at
lower opacity. Nothing is elevated because of where it sits in a hierarchy; things are
elevated because something is true of them.

Three levels of glass, deliberately distinct: cards blur 20px at 1.8 saturation, panels and
the settings dial 16px at 1.6, chips and notes 14px, and the session bar 26px at 1.5 —
the bar is the only element that must stay legible over anything at all.

The Read register has **no shadows whatsoever**. Depth there is a single tonal step (card
`#F6F8FB` on paper `#E7EBF1`) plus a 1px rule, and that is the entire vocabulary.

### Shadow Vocabulary

- **Rest** (`0 1px 0 rgba(255,255,255,.45) inset, 0 10px 26px -20px rgba(27,20,64,.6)`):
  a lit top edge and the faintest possible anchor to the page.
- **Doing** (`0 1px 0 rgba(255,255,255,.5) inset, 0 16px 34px -18px var(--solid)`): tinted
  with the card's own amber, paired with `scale: 1.015`.
- **Done** (`0 1px 0 rgba(255,255,255,.22) inset, 0 12px 30px -20px var(--solid)`): tinted
  green, dimmer inset — a finished card recedes.
- **Inset rim** (`0 0 0 1px rgba(255,255,255,.5) inset`): panels, chips and pills. A
  one-pixel highlight standing in for a border on translucent surfaces.
- **Session bar** (`0 -18px 40px -24px rgba(14,10,34,.8)`): upward, separating the bar from
  the content it is deliberately not covering.

### Named Rules

**Shadow Is State, Not Height.** Surfaces are flat at rest. A shadow appears because a
movement is being done or has been completed, and it is tinted with that state's own colour.
A shadow added to signal importance, hierarchy, or hoverability is wrong here.

**The Spotlight Rule.** While a session runs, everything that is not the active card recedes
toward the paper (`opacity: .3`, `saturate(.5)`) and the backdrop photograph calms with them
(`opacity: .4`, `saturate(.25)`). Dimming is done element by element, never with an overlay —
these cards are glass, and a scrim laid behind them would be sampled by their own
backdrop-filter, darkening the one card the spotlight exists to keep lit. The active card
stops being glass and goes fully opaque for the same reason. Under `forced-colors` the dim
tokens reset to `1` and `none`: the palette is the user's, and dimming it is not ours to do.

## Shapes

Two form languages, and nothing between them.

**Execute** is soft and continuous: 26px cards, 22px panels and notes, 20px video frames,
16px block actions, 15px badges, and full 99px pills for every control that can be pressed —
tabs, chips, the check, the hold, the gear, the transport buttons. Borders are mostly
absent; where a card needs an edge it is a 1px rim derived from the state colour at 72%
toward white, or a white inset highlight. The session bar is the one asymmetric shape in
the system (`18px 18px 0 0`), because it is attached to the bottom of the screen.

**Read** is rectilinear and printed: zero radius everywhere, 1px `#CBD4E0` rules, a 2px ink
rule under the masthead, dashed gridlines for the load axis, and a selection state drawn as
a 1.5px box with a 3px bottom edge rather than a fill. Bars in the block chart are plain
rectangles; only the Execute histogram rounds its bar tops (3px, top corners only).

### Named Rules

**The Two-Radius Rule.** A surface is either a 26px glass card or a 0px printed panel.
Nothing in this system has an 8px corner. Choosing a radius means choosing a register.

**The Pill Rule.** If it can be pressed and it holds a word, it is a 99px pill. If it holds
a glyph, it is a circle. Rectangular buttons exist only in the end-of-session prompt row,
where the words would not fit a 34px circle.

## Components

### Buttons

- **Shape:** fully round pills (99px) for words, circles for glyphs. No borders on filled
  actions; a white inset hairline (`0 0 0 1px rgba(255,255,255,.45) inset`) instead.
- **Primary — the hold / watch action:** Chip Veil background, foreground solved against
  that composite at 4.5:1, 11px 17px padding, 13px/800 type.
- **Check:** the same veil, 8px 12px padding, 11px/900 uppercase at .09em tracking. Gains a
  `✓ ` prefix via `::before` when done — the tick is content generated by state, not a
  second icon.
- **Press:** `transform: translateY(2px)` over 120ms. Every pressable thing in the app uses
  this and only this. There is no hover-lift.
- **Focus:** `3px solid` Midnight Violet at 3px offset, globally, via `:focus-visible`.
- **Transport (session bar):** 34px circles, `rgba(255,255,255,.20)` on a 35% white border,
  with inline SVG glyphs filled `currentColor`. Never `⏸`/`⏭` as text — those render as
  colour emoji on many Androids, which fights the glass and ignores the button's colour.
  The primary transport button inverts to solid white and gets dark icons for free.

### Cards / Containers

- **Corner Style:** 26px (`.ex`), with the flipped back face at 25px to sit inside the rim.
- **Background:** a 152° linear gradient in OKLAB from the state tint mixed 55% toward white,
  down to the tint itself — at 24% alpha at rest. Doing and Done add a
  `radial-gradient(120% 80% at 12% 0%)` white sheen at 18–30%.
- **Interaction:** at rest a card is a window onto the backdrop; on hover, focus-within,
  active or pinned it swaps to the strictly-lighter opaque gradient, so the same solved text
  colour still holds. Opacity is never raised to protect text — the scrim already bounds
  how dark the backdrop can get, so the text is solved against the resting composite instead.
- **Internal Padding:** 16px, with the flipped back face using `inset: -16px` to cancel it
  exactly, so the video runs edge to edge from the tile's own boundary.
- **Badge:** 44px square, 15px radius, filled with the state colour raised until it carries
  Midnight Violet at 4.5:1.

### Navigation

- **Tabs:** a horizontally scrolling pill strip with hidden scrollbars, 10px 14px padding,
  900 weight at 13.5px. Unselected is glass on Ink-2; selected inverts to solid Midnight
  Violet on white. Under `forced-colors` the selected tab becomes a 2px `Highlight` border
  on `Canvas` rather than a fill, because a fill would be stripped.
- **Top bar:** one line — a 16px title that never changes, the date that does, then a Today
  button that exists only when you are not on today, and the gear. A button that says
  "today" while you are looking at today is a button that does nothing.

### Panels & Notes

- **Panel:** Glass Pane at 22px radius, 16px 17px padding, white inset hairline, blur 16px.
- **Note:** the same material at 14px blur with a `rgba(255,255,255,.55)` border. Notes carry
  explanatory prose at 13.5px/500 with bold in Midnight Violet for the load-bearing clause.

### Signature Component — The Session Bar

A slim fixed bar, not a sheet. Everything is one row deep: a phase label and step count on
the top row, the exercise name below them, and the clock and transport held against the
right across both rows. What the shape buys is the screen behind it — the exercise being
timed stays visible while the timer runs, which a full-height sheet made impossible. Column
two is `minmax(0, 1fr)` so a long name shrinks and ellipses instead of shoving the clock off
the edge. Progress is drawn as a 3px line along the bar's own top edge, so it reads as the
bar filling rather than as one more widget. Its gradient is generated per session by `sky()`,
which rotates hue with progress and re-solves its own foreground each time. It enters with
`transform: translateY(100%)` over 340ms on `cubic-bezier(.2,.85,.25,1)`.

### Signature Component — The Flip

An exercise card swaps to a video face by rotating 650ms on `cubic-bezier(.2,.75,.2,1)`
with `preserve-3d`. Identity transforms (`translate: 0; rotate: 0deg; scale: 1`) sit on the
base state deliberately — applying one only on a state change would move the element into a
new stacking context mid-transition. Under `prefers-reduced-motion` the flip is not slowed,
it is **replaced**: the back face drops into normal flow with negative margins doing the
edge-to-edge job that `inset: -16px` does in the animated version.

### Signature Component — The Block (Read register)

Six weeks of prescribed training as one row of flexible columns: height is the day's load,
the stacked fill is where that load was spent on the intensity ramp, and a rest day is a
3px dotted baseline rather than a gap. Dashed gridlines carry the load scale, because a
shape without a scale is decoration. It builds itself once on arrival — `scaleY(.04)` to
full over 500ms from the bottom edge — and only under `prefers-reduced-motion: no-preference`.

## Do's and Don'ts

### Do:

- **Do** derive every foreground from a solver against Worst-Case Backdrop (`#939199`).
  `inkFor` for text on glass, `fade` for a secondary tone, `fill` for a surface that must
  carry a known foreground.
- **Do** keep hue meaning one thing per register: state in Execute, intensity in Read.
- **Do** tint state shadows with the surface's own solid (`var(--solid)`), never with black.
- **Do** press with `translateY(2px)` over 120ms — the single interaction physic in the app.
- **Do** write every `prefers-reduced-motion`, `prefers-reduced-transparency` and
  `forced-colors` branch as a designed state. Glass has no meaning in forced colours; those
  branches replace it with `Canvas` plus a `CanvasText` border, and mark active and done
  cards with `Highlight` and `LinkText` borders instead of fills.
- **Do** ship a `@supports not (backdrop-filter)` path that falls back to opaque panels.
- **Do** quote Stryd's prescription with `pre-wrap` and leave its own formatting intact.
- **Do** keep small Read-register text at or above 4.59:1 — the measured value, not the
  one that looks right.

### Don't:

- **Don't** author a foreground hex on a glass surface. It bypasses the only thing keeping
  the app legible over arbitrary footage.
- **Don't** colour anything by identity. Nine cards must never mean nine hues.
- **Don't** introduce a dark theme, a neon accent, or a carbon-fibre texture. This is a
  light interface on pale paper; dimming during a session recedes *toward* the paper, and
  darkening it would invert the whole app for the length of a hold.
- **Don't** add streaks, badges, confetti, closing rings or congratulatory copy. The app
  reports what happened.
- **Don't** use an 8px radius. Pick a register.
- **Don't** put a background on `body` — it paints over the negative-z-index backdrop.
- **Don't** dim with an overlay. Glass samples what is behind it, so an overlay darkens the
  very card the spotlight exists to keep lit.
- **Don't** let anything on the session bar wrap, or grow past the clock.
- **Don't** add a hover-lift, a second press physic, or a shadow that signals importance
  rather than state.
- **Don't** widen the Execute column past 620px without moving the flipped card's height
  derivation with it.
