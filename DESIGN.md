---
name: Post-run
description: The day as a printed programme — hue names the channel, treatment names the state.
colors:
  silver: "#D9DDD9"
  plane: "#EFF1EE"
  plane-spent: "#E1E4E0"
  ink: "#191E1B"
  rule: "#5A605C"
  name-ink: "#4C524E"
  channel-pre: "#5FA842"
  channel-run: "#569ADF"
  channel-post: "#E8842A"
  channel-log: "#A587D0"
  channel-settings: "#8E9893"
  band-pre: "#077900"
  band-run: "#006BB3"
  band-post: "#AF4600"
  band-log: "#775BA3"
  band-settings: "#5B6560"
typography:
  display:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "clamp(34px, 10.5vw, 46px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.03em"
    fontVariation: "'wdth' 112"
    fontFeature: "tabular-nums"
  headline:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "26px"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 100"
  title:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 100"
  body:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
    fontVariation: "'wdth' 100"
  label:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.16em"
    fontVariation: "'wdth' 87"
  counter:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "10.5px"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.12em"
    fontVariation: "'wdth' 75"
    fontFeature: "tabular-nums"
rounded:
  none: "0"
spacing:
  gutter: "2px"
  1: "4px"
  2: "8px"
  3: "12px"
  4: "16px"
  5: "20px"
  6: "24px"
  8: "32px"
  10: "40px"
components:
  row-todo:
    backgroundColor: "{colors.plane}"
    textColor: "{colors.name-ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "12px"
  row-doing:
    backgroundColor: "{colors.channel-post}"
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.none}"
    padding: "12px"
  row-done:
    backgroundColor: "{colors.plane-spent}"
    textColor: "{colors.rule}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "12px"
  badge:
    backgroundColor: "{colors.plane}"
    textColor: "{colors.name-ink}"
    rounded: "{rounded.none}"
    width: "44px"
    height: "44px"
  badge-doing:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    width: "104px"
    height: "104px"
  tab:
    backgroundColor: "{colors.plane}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "8px 8px 6px"
    height: "48px"
  tab-selected:
    backgroundColor: "{colors.channel-post}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "8px 8px 6px"
    height: "48px"
  button-run:
    backgroundColor: "{colors.channel-post}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "16px"
    height: "64px"
  button-hold:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.plane}"
    rounded: "{rounded.none}"
    padding: "8px 14px"
    height: "48px"
  button-watch:
    backgroundColor: "transparent"
    textColor: "{colors.rule}"
    rounded: "{rounded.none}"
    padding: "8px 14px"
    height: "48px"
  chip-state:
    backgroundColor: "{colors.plane}"
    textColor: "{colors.rule}"
    typography: "{typography.counter}"
    rounded: "{rounded.none}"
    padding: "8px 10px"
    height: "48px"
  section-marker:
    backgroundColor: "{colors.channel-post}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "5px 8px"
  panel:
    backgroundColor: "{colors.plane}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "16px"
  carriage:
    backgroundColor: "{colors.channel-post}"
    textColor: "{colors.ink}"
    typography: "{typography.display}"
    rounded: "{rounded.none}"
    padding: "12px 14px 13px"
---

# Design System: Post-run

## Overview

**Creative North Star: "The Printed Programme"**

This is Otl Aicher's 1972 Munich programme applied to a training day. The page is
not a stack of cards on a background; it is a sheet of silver paper with bands
printed on it. There is no glass, no blur, no lift, no rounded corner and no
drop shadow anywhere in the build. What separates one thing from another is a
value step, a 1–2px inset rule, and two pixels of bare ground. Everything sits
on a 4px unit and a single variable grotesque whose *width* axis — not its
weight — does most of the expressive work.

Two variables carry all the meaning and never trade jobs. **Hue names the
channel**: which part of the day you are looking at. **Treatment names the
state**: outlined is waiting, flooded is happening, receded is finished. A green
day and an orange day are the same design proved twice, not two palettes.

The palette itself is the system's real signature: almost nothing in it is
authored. Five seeds are pushed through contrast solvers at boot and again on
every channel change, and what reaches the screen is the solved output. Two of
the four channel seeds never appear on screen at all. The document below records
what is painted, and names the seed separately where they differ.

The world it refuses is the one this file replaced: translucent violet cards
floating over a photograph, with radii and shadows doing the separating.

**Key Characteristics:**
- Silver ground (#D9DDD9), never white, never a dark field
- Square corners everywhere — `border-radius: 0` without a single exception
- 4px unit; a 2px gutter of bare ground between adjacent bands
- One self-hosted variable font; four width stops (75 / 87 / 100 / 112)
- Every colour solved against its ground before it ships, never chosen by eye
- No shadows, no blur, no backdrop-filter — inset rules only
- 22 authored pictograms on a 0/45/90 raster, one per movement
- Accessibility branches are designed states, not fallbacks

## Colors

Aicher's 1972 spectrum on a silver ground: light blue, green, orange, violet —
no red, and no black field. Nothing here is a decorative hue; every colour is
either the ground, the ink, or a channel.

### Primary

The four channels. Each has two painted forms: the **field** (solved to carry
ink at 5.5:1, used for flooded rows, tabs, the run button and the session
carriage) and the **band** (the same seed solved to carry white at 5.5:1, used
only for the poster band at the top of the page). Exactly one channel is on
screen at a time.

- **Drill Green** — field `{colors.channel-pre}` / band `{colors.band-pre}`: the
  pre-run channel. Seed and field are identical; the seed already carried ink.
- **Run Blue** — field `{colors.channel-run}` / band `{colors.band-run}`: the run
  channel. **Seed `#2E7CBF` is never painted** — it fails 5.5:1 against ink and
  the solver brightens it to the field value.
- **Mobility Orange** — field `{colors.channel-post}` / band `{colors.band-post}`:
  the post-run core and mobility channel. Seed and field are identical.
- **Log Violet** — field `{colors.channel-log}` / band `{colors.band-log}`: the
  progress channel. **Seed `#7E63A8` is never painted**; the solver brightens it.

### Secondary

- **Device Grey** — field `{colors.channel-settings}` / band
  `{colors.band-settings}`: the settings channel. It is a channel by mechanism
  but deliberately the only desaturated one, because settings is not part of the
  day. Seed `#5B6560` is painted only as the band; the field is brightened.

### Neutral

- **Silver** `{colors.silver}`: Aicher's *silber*. The page ground, the
  scrollbar track, and the value every foreground in the system is proved
  against. The page is grey, not white.
- **Plane** `{colors.plane}`: the raised sheet a waiting row, panel or note is
  printed on. One step lighter than the ground.
- **Spent Plane** `{colors.plane-spent}`: a finished row. Deliberately *between*
  the ground and the plane — a done row recedes toward the paper, never away
  from it.
- **Ink** `{colors.ink}`: all body copy, all rules of weight, the hold button
  field, and the carriage's progress rule. Near-black with a green cast; never
  pure black.
- **Rule** `{colors.rule}`: solved at 3:1 against the silver for non-text
  boundaries — rims, chip outlines, dividers. The same solved value also carries
  secondary text at 4.69:1, so one painted grey serves both jobs.
- **Name Ink** `{colors.name-ink}`: solved at 7:1 on the plane. Movement names
  and other primary text inside a waiting row.

### Named Rules

**The Solved-Not-Chosen Rule.** No colour ships as authored. `dressPage()`,
`setChannel()` and `solveStates()` push every seed through `fill`, `inkFor` and
`fade` — walking the value until it clears its contrast target against its
actual ground — and the walked value is what is painted. If a hue cannot carry
its type, it is moved until it can; it is never shipped and excused. Record and
reuse the painted value, never the seed.

**The One Channel Rule.** Exactly one channel hue is on screen at a time. The
tab strip is the single licensed exception: it is the one place all four appear
at once, because it is the map. Anywhere else, two channel hues in the same
viewport means the system is contradicting its own first rule.

**The No-Red Rule.** Aicher removed red from the 1972 spectrum and nothing here
needs it, because hue names *which channel you are in* and never *how urgent
something is*. Urgency carries by weight and rule instead: the expired-token
line goes to full ink, weight 700, with a 2px underline. No red is authored
anywhere in the stylesheet or the app script.

## Typography

**Display Font:** Archivo Variable, self-hosted (`fonts/archivo-var.woff2`),
weight axis 100–900, width axis 62–125%
**Body Font:** the same face
**Label/Mono Font:** the same face, condensed, with `font-variant-numeric:
tabular-nums`

**Character:** Univers is Aicher's face and is not free; Archivo is the closest
grotesque with a real width axis, and the width axis is the part that matters —
the 1972 programme is a width/weight *matrix*, not one cut. One family does
every job here; `font-synthesis: none` means the browser is never allowed to
fake a stop the file does not have.

### Hierarchy

- **Display** (700, `clamp(34px, 10.5vw, 46px)`, wdth 112, -0.03em, tabular):
  the session clock in the carriage, and the dial's second-count at 28px. The
  only extended cut in the system, reserved for numerals read at arm's length.
- **Headline** (600, 26px, wdth 100, -0.012em): the movement name in a row that
  is being done. Steps down to 22px below 360px.
- **Title** (600, 19px, wdth 100, -0.012em / 1.12): the movement name at rest,
  the plan title, the run button (17px).
- **Body** (400, 13.5px / 1.6): notes, prescriptions, verdicts, log entries.
  Doses run at 13px.
- **Label** (600, 11px, wdth 87, 0.16em, lowercase): section markers, `h2`,
  `h3`, the greeting line. The system's own speaking voice.
- **Counter** (500, 10.5px, wdth 75, 0.12em, tabular): tab counts, the carriage
  step count, the row sequence number at 10px/0.14em. Machine metadata.

### Named Rules

**The Width-Axis Rule.** Emphasis moves along the width axis before it moves
along weight. Four stops, and each means something: **75%** is machine metadata
(counts, sequence numbers), **87%** is the system's own voice (every label,
every button word, every heading), **100%** is content (movement names, prose),
**112%** is the clock. A new size that does not land on one of these four stops
is not part of the ramp.

**The Lowercase Programme Rule.** Every system label is `text-transform:
lowercase` — the masthead, headings, tabs, buttons, state chips. Content is not:
an exercise name keeps the capitals the plan gave it. Lowercase is how the
interface signals that it is the interface talking.

## Layout

One column, capped at **620px**, centred at every viewport width. There are no
`min-width` breakpoints: widening the phone app would make a worse phone app,
not a web one. The only responsive branch is a **360px** step-down that tightens
tab padding and drops the flooded row's headline from 26px to 22px and its
pictogram from 104px to 80px.

The rhythm is a **4px unit** (`--u`) and every measure is a multiple of it: body
side padding 16px, row padding 12px, section spacing 28–32px, group spacing
24px, the bottom safe-area reserve 40px plus `env(safe-area-inset-bottom)`.
Touch targets are 44px minimum and 48px for anything hit mid-session; the run
button is 64px.

The one measure that is not a multiple of the unit is the **2px gutter** between
adjacent bands — rows, tabs, action buttons, panels, chips. It is a printer's
gutter, not a margin: two pixels of bare silver showing between two printed
things.

The poster band is a fixed **132px** at the top of the page: the running
photograph, desaturated and printed in the channel's band ink via
`mix-blend-mode: multiply`, with the masthead knocked out of it in white. It is
the largest field on screen and it obeys the first rule — it re-solves whenever
the channel changes.

### Named Rules

**The Two-Pixel Gutter Rule.** Adjacent surfaces are separated by 2px of ground,
never by a margin and never by a border between them. Bands touch the column
edge; the gutter is the only thing between them.

**The Single Column Rule.** One 620px column at every width. Do not introduce a
wide-viewport grid, a sidebar, or a two-up layout on this surface.

## Elevation & Depth

**This system has no elevation.** There is not one drop shadow, one blur radius,
or one `backdrop-filter` in the file. Every `box-shadow` declaration is
`inset 0 0 0 Npx` — a printed rule drawn inside the box, occupying no space and
casting nothing.

Depth is entirely a **value step on the silver**, in three positions:

- **Plane** `{colors.plane}` — forward. A waiting row, a panel, a note.
- **Ground** `{colors.silver}` — the paper. What shows through the gutters.
- **Spent** `{colors.plane-spent}` — back. A finished row, sitting between the
  ground and the plane so it recedes toward the paper rather than turning into
  the heaviest field on the page.

A flooded row escapes the value system entirely: it drops its inset rule and
becomes a solid field of the channel, which is what makes it read as *on* rather
than *raised*.

### Shadow Vocabulary

- **Hairline rim** (`box-shadow: inset 0 0 0 1px {colors.rule}`): the boundary
  of a waiting or finished row, a chip, a panel.
- **Heavy rim** (`box-shadow: inset 0 0 0 2px`): the pictogram block's outline
  and the dial's frame — the two places a boundary is structural rather than
  incidental.

### Named Rules

**The No-Shadow Rule.** Nothing in this system casts. If a surface needs to read
as separate, give it a value step, an inset rule, or 2px of gutter. A
`box-shadow` with a non-zero offset or blur is a bug in this world, not a style
choice.

**The Three-Value Rule.** Depth has exactly three positions — plane, ground,
spent — and they are already spent. Do not introduce a fourth surface value.

## Shapes

`border-radius: 0` on every element in the file: rows, buttons, tabs, chips,
inputs, the video frame, the carriage, the pictogram block, the chart bars, the
legend swatches. There is no radius scale because there is no radius.

Boundaries are **rules, not outlines**: 1px inset for incidental separation, 2px
for structural, 3px for the tab's top edge (the one place a channel hue appears
as a line rather than a field). The section heading is a filled ink chip of the
channel colour with lowercase label type knocked out of it.

The system's recurring silhouette is the **band**: a full-width rectangle, 12px
of padding, a 44px square pictogram block at the left, name and dose in the
centre, a state chip at the right. Everything on the page is either a band, a
chip, or a rule.

### Named Rules

**The Square Corner Rule.** Every corner in this world is square. There is no
"just this one" — a single rounded element reads as an element from a different
system that wandered in.

**The Raster Rule.** Pictograms are drawn on a 44×44 grid using strokes at 0°,
45° and 90° only, one 4px stroke width throughout, `stroke-linecap: butt`,
`stroke-linejoin: miter`, and a filled circle for the head. Twenty-two are
authored, one for every movement the plan can name; the generic figure is the
fallback and is itself drawn.

## Components

### The Movement Row (signature component)

A printed band, not a card. It is the primary action: the row *is* the control.
Square corners, 12px padding, 2px of gutter below it, and a state that is
carried by treatment rather than by hue.

- **To do (outlined):** plane field `{colors.plane}` with a 1px inset rule in
  `{colors.rule}`. The pictogram block is 44px, plane-filled, outlined in the
  **channel** colour at 2px — the channel marks the work still waiting, not the
  work already done, because in a session the eye has to land on the next undone
  thing. Name at Title, dose at 13px in `{colors.rule}`, sequence number at
  Counter.
- **Doing (flooded):** the entire band floods with the channel field and the
  inset rule is removed. Everything on it is knocked out in ink. The pictogram
  goes to **104px**, the name to Headline (26px), the dose to 16px, and the
  block's fill drops to transparent with an ink outline. Mid-hold the row is
  read at arm's length by someone breathing hard, so what is on screen is the
  movement rather than a caption about it.
- **Done (receded):** the band drops to `{colors.plane-spent}`, keeps its 1px
  rule, carries **no hue at all**, and loses its shelf of action buttons. It
  keeps the state chip — the work has to be undoable — and the chip grows a
  drawn tick (two 2px borders rotated -45°, not a glyph). A finished row is a
  record, not a target.
- **Flip:** tapping *Show me* rotates the band 180° on Y over 550ms
  (`cubic-bezier(.2,.75,.2,1)`) to a demonstration clip on the back face. Under
  `prefers-reduced-motion` the rotation is replaced by a straight
  front/back swap with no transform at all.

### The Channel Tabs

Four tabs, `flex: 1 1 0`, 2px apart, 48px tall, left-aligned, lowercase at
12.5px/wdth 87. Each carries a **3px top rule in its own channel colour** at all
times — this is the only place all four hues coexist. The selected tab fills
with its channel colour; the others stay plane. A count sits under each name at
Counter (10.5px/wdth 75). The strip carries 5px of internal padding so an
outline focus ring is not clipped by its own overflow scroller.

### Buttons

- **Shape:** square (0 radius), universally.
- **Run it (primary):** the loudest field in the column — full-width, 64px
  minimum, flooded in the channel colour with ink type at 17px/wdth 100, a
  lowercase Counter-voice sub-label beneath, and a drawn play triangle. It
  inverts on press (ink field, channel type).
- **Hold / Start:** ink field, plane type, 48px, 13px/wdth 87. Inverts to the
  channel colour on press.
- **Show me / YouTube (ghost):** transparent with a 2px inset rule in
  `{colors.rule}`; inverts to a solid ink field on press.
- **State chip:** 48px, 2px solid rule, plane field, Counter voice, lowercase.
  It always spells the state in words.
- **Carriage controls:** 48px squares, transparent, 2px `currentColor` border,
  with inline-SVG transport glyphs. The primary control fills with ink and takes
  the channel colour for its icon.
- **Focus:** a 3px solid ink outline at 2px offset everywhere — except on the
  poster band, where the ink ring measured 1.22:1 and the ring switches to
  white.

### The Session Carriage (signature component)

A fixed bottom bar, one row deep, that appears when a session starts. It is a
**flat field of the channel's own ink** — no gradient, because Aicher's posters
have none. It slides up on a 300ms `cubic-bezier(.2,.85,.25,1)` translate and
sits at the bottom so the movement being timed stays on screen.

Four-column grid: phase label (Label voice, faded ink at 4.5:1) and step count
top-left, movement name below, the clock at Display scale (up to 46px, wdth 112,
tabular) at the right, transport controls at the far right. Progress drives a
**4px ink rule along the top edge** — a bar, not a hue shift nobody can read
mid-hold. *Stop* gets its own 12px gutter away from *Pause*, because two pixels
apart with wet hands is a mis-tap that costs the work.

### The Hold Dial

A plane band framed by a 2px inset ink rule. Two 44px ink squares flanking a
Display-scale numeral (28px, weight 700, wdth 112, tabular, 72px minimum width
so the number does not shift the layout as it counts). The label sits between
them at 13px with a 11.5px sub-line.

### Panels and Notes

- **Panel:** plane field, 16px padding, 1px inset rule. Its `h3` carries a 2px
  ink underline. Stacked panels are 2px apart.
- **Note:** plane field, 16px padding, and a **2px ink rule along the top edge
  only** — the one asymmetric treatment in the system, and it marks editorial
  voice rather than data.

### Charts

Both the power histogram and the zone bar are drawn as a **single-hue ramp of
the current channel**, mixed in LCH from white toward the flooded-row colour
(0.22 → 1.0 for the histogram, 0.25 → 1.0 for the zone bar). Bars are square,
1px apart, on a 2px ink baseline; the critical-power line is a dashed 2px ink
rule. There is no categorical palette anywhere in this system.

### The Spotlight (signature behaviour)

While a session is running, `body.running` drops everything that is not the
movement being done to **opacity 0.34 and `saturate(0.35)`**, and the poster
band further to **opacity 0.45 / `saturate(0.2)`**, over a 300ms linear fade.
The flooded row stays at full strength, so the only thing at full colour on the
page is the thing you are doing.

This is behaviour, not decoration. It is the visual half of the product's whole
promise — a session completed with the phone on the floor and never touched — and
it runs alongside a screen wake lock and audio cues so the page can be read from
across the room without being woken. It recedes toward the **silver**, never
toward black: this is a light interface and inverting it for the length of a hold
would be worse. Under `forced-colors` the dimming tokens are set to
opacity 1 / `none`, because dimming in a user's own two colours destroys legibility
rather than focusing it.

### Accessibility States

These are designed states, not degradations, and each one is a legitimate
expression of the world.

- **`prefers-reduced-motion`**: all transitions off; the row's 3D flip becomes a
  face swap; the carriage appears without sliding.
- **`prefers-reduced-transparency`**: the poster photograph is removed and the
  band becomes a flat field of channel ink — still an Aicher poster.
- **`forced-colors`**: backgrounds strip to `Canvas`, type to `CanvasText`, and
  the whole system falls back to a border language that still separates. A
  flooded row becomes a 3px `Highlight` border; a done row becomes 3px
  `LinkText`. Chart bars and the pictogram block set `forced-color-adjust: none`
  so the drawing survives. The spotlight's dimming is switched off entirely.

## Do's and Don'ts

### Do:

- **Do** solve every new colour against its actual ground before shipping it —
  text at 4.5:1, primary text at 7:1, non-text boundaries at 3:1, and anything
  on a flooded channel field at 5.5:1. Use `fill`, `inkFor` and `fade`; do not
  eyeball a value.
- **Do** record and reuse the **painted** value, never the seed. `#2E7CBF` and
  `#7E63A8` are inputs to the solver and appear nowhere on screen.
- **Do** put one channel hue on screen at a time, and let the tab strip be the
  only place all four meet.
- **Do** signal state by treatment — outlined, flooded, receded — and always
  spell the state out in words as well.
- **Do** move emphasis along the width axis (75 / 87 / 100 / 112) before
  reaching for another weight.
- **Do** set every system label in lowercase, and leave content's capitals alone.
- **Do** separate surfaces with 2px of bare ground, a value step, or an inset
  rule.
- **Do** draw new icons and pictograms on the 0/45/90 raster at one 4px stroke
  width, and give every movement its own.
- **Do** keep touch targets at 44px minimum, 48px for anything used mid-session.
- **Do** ship the reduced-motion, reduced-transparency and forced-colors
  branches with any new surface. They are part of the design, not a cleanup pass.

### Don't:

- **Don't** add a `border-radius`. Anywhere. The vocabulary is one value: 0.
- **Don't** add a drop shadow, a blur, or a `backdrop-filter`. Every shadow in
  this system is `inset 0 0 0 Npx` and casts nothing.
- **Don't** introduce red. Hue names the channel, never urgency; urgency carries
  by weight, full ink, and a rule.
- **Don't** signal state by changing hue, or by colour alone.
- **Don't** put a categorical palette in a chart. Charts are a single-hue ramp
  of the channel currently on screen.
- **Don't** paint a dark field. The poster band is the one dark thing in the
  system, and the spotlight recedes toward the silver, never toward black.
- **Don't** let a letter, digit or emoji stand in for a drawn mark.
- **Don't** widen the column past 620px or add a wide-viewport grid to this
  surface.
- **Don't** invent a type size outside the ramp, and don't let the browser
  synthesise a weight or width the font file does not carry
  (`font-synthesis: none`).

<!-- Scope: this file documents the phone application at ./index.html. The
     desktop surface at web/index.html is a separate artifact with its own type
     pairing and is not governed by this system. -->
