# Releases

## v13 — 2026-09-07

Fixes the remaining horizontal split on Shredder's Technodrome stage. The
v12 adjustment left a second scrolling-table displacement in place, and
the cage shared a later lookup in the same handler. V13 aligns the wall
bands and compensates that later lookup so cage movement stays unchanged.
Exactly two bytes differ from v12; the SNES checksum remains `C77F`.

Target SHA-256:
`461290feac2c13846a50b30bf8b69a744a8f0f7b8aca9c5421d1413b619455ae`.

## v12 — 2026-09-07

Full-height and inward-facing portraits, corrected select icons, improved
attack poses, projectile/effect load repairs, bank-safe sprite DMA packets,
dark stage shadows, stage animation repairs, and Leonardo's Japanese night
alley. The initial Shredder scrolling correction was incomplete; use v13.

Source SHA-256 for the incremental v13 patch:
`8811ac47e3dd3a7535383fe561108929aa583e715aa7157aa166b50566141796`.

## Earlier development

The project began with a palette test, followed by Shredder replacing Vega
and a Technodrome replacing the Spanish stage while retaining its cage.
Leo and Raph came next, then seven additional assigned fighters/stages.

The expanded roster revealed shared-resource problems affecting map and
bonus scenes. Subsequent cleanup preserved all 27 scene layouts, repaired
graphics allocation and added full Arcade/bonus coverage. Earlier milestone
patches are not published here; v13 includes the cumulative replacements.
