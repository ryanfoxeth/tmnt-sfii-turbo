# Releases

## v22 — costume-aware turtle captions

Target SHA-256: `fe12e8693eb985e1318f1652a9be837090ad4c4ceff4eaa0fef880eb5749ddba`; SNES checksum: `3527`.

Select and VS gold captions follow alternate turtle costumes: alternate Leo displays DON and alternate Raph displays MIKEY. Aggregate records use shared totals labeled LEO/DON and RAPH/MIKEY. Main labels remain LEO/RAPH. All body, portrait, icon, stage, palette, OAM/DMA and move resources remain v21-exact.

Verification covers: Ten Normal/Turbo main/alternate, swapped-side and mirror UI routes; 7,200 fighter-state frames match v21; ten initial select images are pixel-exact. Six two-KO outcomes verify DON/MIKEY winner captions on both sides, including mirrors; two Arcade loss routes verify costume-aware portrait transitions. A 45,000-frame Arcade route covers all twelve stages, 24 KOs and three bonuses; KO timeline matches v21.

## v21 — alternate turtle palettes

Target SHA-256: `27bab79c6cf21c284f9aa52d396088cdc8f1d8bd7983683d1e51e1a826dc8671`.

Adds bold Donatello-purple Leonardo and Michelangelo-orange Raphael alternate
costumes. Mode-aware palette normalization preserves the blue/red primary
costumes in Normal and Turbo. Moves, hitboxes, graphics, OAM/DMA, stages and
other fighters remain unchanged. Runtime verification covers both modes,
ports, mirrors, alternate defeated portraits, continue routes and a full Arcade
run through all twelve stages and three bonuses. Confirm Leo/Raph with Start
for Don/Mikey. Battle HUD and VS winner banners use temporary DON/MIKEY names;
select/VS bitmap captions, aggregate records and other static names stay LEO/RAPH.

## v20 — stages, projectile graphics and Casey pose loads

Target SHA-256: `69a71550ed6e9badfd4f2b277b4668b575f7d450ab250cd40604c12ea6dc6fbb`.

Scope: Slash's approved Dimension X scrapyard/plain floor with original BG3 foreground fence; Leatherhead's original Brazil scenery with new night palettes and navy backdrop; Casey's hockey-stick Sonic Boom graphics and missing pose 37 auxiliary loads. No moves, hitboxes or gameplay changes.

## v19 — Splinter standing orientation

Target SHA-256: `a1cbd12ab115b81cfd7e970f4e331329715d0168ed0edb2c62a67c8ae5f7aec1`.

Scope: Splinter standing idle poses 000–011 only, using per-object OAM x-reflection/HFLIP metadata. The patch changes 366 bytes total: 362 OAM x/HFLIP bytes plus the SNES checksum. Existing source tiles, DMA, animation timing, palettes, and ROM allocation are retained. Known Super Shredder walking-pose waist gap 004/005 remains open.

## v18 — 2026-09-08

Removes empty lower bands from seven select icons using full-height, face-centered
bust crops. Updates Normal/Turbo and the two custom gray variants; the same icon
art also appears on the Arcade map. All large portraits remain unchanged.

Repairs 192 transparent waist pixels in Super Shredder poses 000–003. Previously
opaque pixel colors, all other body packets, palettes, OAM/DMA, animation timing,
moves and stages are preserved. The observed OAM/VRAM mismatch during debugging
was emulator snapshot timing, not a game DMA defect; no timing patch was made.

Target SHA-256: `0e1e06361f4b21cddf425adb8b9fb072157cb32db1609aef609bcec7cadd7c20`. SNES checksum: `A353`.
Includes original-to-v18 and v17-to-v18 BPS patches. The Python patcher accepts
the verified original/headered input and v12–v17 releases. Historical patches
remain available. See [verification](verification.md) for coverage and limits.

## v17 — 2026-09-08

Corrects Leatherhead and Slash sprite presentation without changing moves,
hitboxes, animation scripts, body palettes or stages. All 85 Leatherhead and
104 Slash body poses were reviewed at fixed native scale. Twenty-nine
Leatherhead poses received source-registration corrections. Slash's importer
now extracts complete connected figures before measuring them, removing source
labels and neighboring fragments that had shrunk the real character; 69 Slash
imports were corrected. Pose 084 is restored from complete predecessor art,
and the kneeling art shared by poses 099/100 is used at one scale.

Seven select icons were reframed: Bebop, Leatherhead, Casey, April, Slash,
Krang and Rocksteady. All twelve large neutral and defeated portraits remain
unchanged from v16. The read-only review of the other ten fighters covers
1,136 OAM entries, including intentional partial and effect cases; it is an
inventory, not an exhaustive live-animation claim.

Target SHA-256:
`f0cf0064765bef202e75d5c7a664ff9406cfdba6e55bbaad16813d7d8ccd9daa`.
SNES checksum: `0DEB`. The patcher accepts the verified original (headered or
headerless) and v12–v16 outputs. Original and v16 BPS patches are included;
v12–v15 inputs are validated through v16, while v16 takes its direct v17
increment. Earlier patches remain available.

## v16 — 2026-09-08

Completes the twelve selected roster slots: Blanka becomes Leatherhead and
Zangief becomes Slash, using the original cartoon designs. Adds body art,
color and defeated icons, independent intact/defeated portraits, names and
quotes. Existing moves and the two original stages remain. Includes all v14
and v15 corrections described below.

The portrait cache moves its temporary map buffers to 7F:E000/E100 to fit
the larger drawings. A Slash source-crop defect and extra crouching sprite
pressure were repaired before release. Normal/Turbo and final mixed Arcade,
bonus and outcome checks are documented in verification.md.

Target SHA-256:
`389c89355c252d3ad5e8dca5f73e66ad23a27254e094e30ce310b1a37371de71`.
SNES checksum: `67B3`. The patcher accepts the exact original or v12–v15
directly; no sequence of upgrade patches is required.

## v15 — 2026-09-07

Retires 87 old decorative stage-animation lists, containing 376 map commands,
across the ten replacement rooms. It uses the game's existing empty list and
preserves Shredder's cage, room scrolling and bonus/ending lists. The patch
changes 176 pointer/checksum bytes. Original Blanka/Zangief animations remain.
The standalone `fix_stage_animation_v15.py` reproduces this change from v14.

Target SHA-256:
`789a855967a399e10590e500566a5a400d775fe32452a6777201d836afb315f7`.
SNES checksum: `56E1`. Stationary, camera, late-KO and full Arcade checks pass.

## v14 — 2026-09-07

Reframes all ten existing TMNT select icons to fill their 19×30 interiors,
preserving opaque backgrounds, gray borders, palettes and allocation padding.
Normal and Turbo sheets are updated. Full portraits and fighting art stay
unchanged. Menu, wall-attack, full Arcade and all three bonus checks pass.

Target SHA-256:
`aacc2ada6569d35711227d83f179f7ff232a442a1a07b534d0499f0971792d91`.
SNES checksum: `54C9`.

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
