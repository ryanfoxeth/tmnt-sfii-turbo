# Technical notes

## V27 private voice tuning

Resources 3D/3E belong exclusively to Super Shredder, actor ID 9. Their four
big-endian tuning words change from 07A8 to 06D2, a requested ratio of about
−2 semitones. All BRR data and pointers, sound envelopes and event sequences
remain exact. No allocation or code changes are needed.

Measured DSP pitch in the focused routes changes from 944 to 848 for P1 and
960 to 848 for P2. Quantization and native route differences mean the live
shift is about −1.86/−2.15 semitones. The original short sample gate remains;
slower playback can still shorten its tail. The moderate option was selected
after audition; it does not replace Sagat's spoken wording.

## V26 private victory samples

Resources 52/53 belong exclusively to fighter ID 11. The new short/long BRR samples occupy 1,278/4,383 bytes within their existing 1,467/4,788-byte slots, with zero-history first blocks, one final end flag and no looping. The short directory loop pointer now points at sample start; the attack sample/directory/instrument stays unchanged. No ROM/APU expansion or code hooks.

Private tuning words 09B6/06D2 yield live DSP pitches 640/800, nominal 5,000/6,250 Hz against encoded rates 5,500/7,000 Hz. This lowers the new source by about 1.65/1.96 semitones after driver quantization. Native event timing and envelopes are unchanged; both clips finish before their former gates. The short clip uses source 0.42–0.83 s with a 40 ms tail fade.

Source: [Turtles in Time arcade Voices](https://sounds.spriters-resource.com/arcade/teenagemutantninjaturtlesturtlesintime/asset/409875/), generic Boss Laugh 1 (not specifically attributed to Shredder). Encoded with [BRRtools](https://github.com/Optiroc/BRRtools), commit `5b809f171d6a8fe436f09cd883f26994e58feb35`. Source recordings and emulator states are not bundled. The tooling license does not license third-party recordings or patch content.

## V25 final-package constraints

The ending starts original native sequence cue 28 and exits with native `F6 Y08` before stock ranking cue 2F and title cue 11. The two audio receipts record 36 full seconds of continuous cue 28 and zero fade-tail RMS/peak before the next native cues.

V25 repairs 204 Super Shredder waist pixels across walking poses 004/005 and patches all twelve native biography text packets. The combined Turbo P1 check covers 1,728 frames with exact actor RAM/OAM and pixel-exact poses 004/005. A 25,000-frame no-input Slash cold boot matches two settled scene00/script06 screens to the v2 reference; it is not a full biography or attract-mode audit. Voices, stage songs and turtle idle remain unchanged. Selective voice work requires user approval; new stage music remains future work. Existing title, map and geography presentation is retained.

## V23 ending player and victory DMA contract

The shared Arcade-ending dispatcher at C0:32F8 now enters a native 65816 player.
It reads the stock winner selector at WRAM1965 and the saved costume at18B5.
For Leo/Raph, alternate selection means costume minus mode1C84 equals20hex;
this preserves the native Turbo00/20 and Normal20/40 costume convention.
Fourteen packets occupy previously unused audited ROM ranges302000..30F000
and313000..31CC00; code/text/font data stay within31D000..320000. The ROM
remains4MiB. Do not overwrite these reservations with an older whole-bank tool.

Each still uses192 4bpp tiles, a16x12 tilemap and three16-color BG palettes.
BG1 art occupies VRAM2000..3800, its map8000, and palette groups2..4. Private
BG3 glyphs use4000..4800 and map7000; the original font atA000 stays intact
for ranking/menu restoration. Native text uses two8x8 tiles per8x16 glyph.
The ordinary scanline IRQ must remain enabled: it releases frame gate1842.
NMI-only mode81 freezes the scheduler after the first ending page; modeB1
and the standard non-split NMI route preserve normal frame progression.

Mikey/Raph victory pose073 retained its OAM and graphics but lost one DMA
record in an earlier turtle repack. Its two loads are now3A1380/1664bytes to
VRAME000 followed by3A2D80/1984bytes toE400. The second packet covers the
OAM's otherwise missing tiles42..93. The descriptor uses owned table slack
at4097A..40984. Preserve that auxiliary load in future body repacks.

## V20 stage and projectile ownership

Slash's new scenery uses BG1 with BG2 blank. The original BG3 foreground fence
and center-post object remain. Four stage-exclusive decorative animation lists
are retired. Audit all 27 scene layout graphs **and** all 27 graphics-loader
streams: Zangief's original compressed graphics also serve bonus scene 13.
V20 relocates Slash's new art and redirects only the battle-stage loader,
leaving the shared bonus graphics and its loader intact.

Leatherhead preserves the original stage graphics, maps and animation lists.
Seven background palette groups and the room-local backdrop source change to
night colors. Fighter and shared HUD palettes stay unchanged.

Casey's Sonic Boom auxiliary graphics belong to release pose 037. The prior
body repack omitted two loads; v20 restores them with twelve hockey-stick tiles
in unused reserved ROM space. P1 uses VRAM EC00/EE00 and P2 uses FC00/FE00.
The native flipping animation, speeds, hitbox and damage remain; Flash Kick is
unchanged. Detached effects need live tracing as well as body-pose checks.

## V17 character and cache contracts

Leatherhead occupies Blanka's ID2 slot; Slash occupies Zangief's ID6 slot.
Both use private body-packet allocations with shared effects protected, and
all raw DMA sources stay inside a 64 KiB bank. V17 retained both original stages;
v20 replaces Slash’s scenery and gives Leatherhead’s riverside a night palette.
V17 corrects 29 Leatherhead and 69 Slash body imports after fixed-scale review
of all 85 and 104 respective poses. Slash source bounds are measured from the
whole connected figure rather than a nominal cell, so labels and neighboring
fragments cannot shrink a pose. Pose 084 recovers complete predecessor art;
the cross-cell kneeling art for poses 099/100 is extracted once and retains one
scale. The other ten fighters and all 27 original/custom scene resource streams
are checked for preservation before merging the recorded components.

The complete portrait cache is 55,936 bytes starting at 7F:0100. Both temporary
map buffers move to 7F:E000/E100 through four stores and two queued DMA-source
operands, leaving 1,152 bytes of slack. An unrelated static C000 descriptor
must not move. The large portraits are separate neutral/defeated images stored
facing right; the original renderer mirrors right-side screen positions.

Small icons use opaque 19×30 interiors, gray borders and transparent allocation
padding. V17 reframes Bebop, Leatherhead, Casey, April, Slash, Krang and
Rocksteady while leaving all twelve large neutral/defeated portraits byte-exact
v16. Two previously unused regions within the existing 64-tile gray-icon buffer
hold Leatherhead and Slash's defeated icons. This does not enlarge that VRAM
allocation. Leatherhead uses `LEATHER` where narrow captions cannot fit his full
name; `LEATHERHEAD` is retained in the HUD and records.

Static importer round-trips alone do not establish visible correctness. The
first Slash source crop clipped limbs to the old Zangief rectangle, yet the
truncated art round-tripped perfectly. Whole-cell extraction before native
registration fixed the actual cause; live DMA and animation were then checked.
See the retained [generated art](../art/v16/README.md), the v17
[geometry review](../art/v17/README.md), and [verification](verification.md).

## Base-game contract

This remains the SNES game engine. Replacement art follows existing gameplay,
move timing, hitboxes and character slots. It is not a new engine or an extra
roster-slot implementation.

The project works against the **Europe/PAL 1.0** revision. SNES data is highly
version-specific, so a filename alone is not sufficient identification.

| Input | SHA-256 |
| --- | --- |
| Original, headerless | `b8ee1b5b9deae5c84fa209815515030109cc271b645a18de882aaf1b254cda1f` |
| Original, 512-byte copier header | `98d0b789a8a0c25bf82c777cba7289faa14365133cb7ea9d822005a1fdca3101` |
| v12, headerless | `8811ac47e3dd3a7535383fe561108929aa583e715aa7157aa166b50566141796` |
| v16, headerless | `389c89355c252d3ad5e8dca5f73e66ad23a27254e094e30ce310b1a37371de71` |
| v17, headerless | `f0cf0064765bef202e75d5c7a664ff9406cfdba6e55bbaad16813d7d8ccd9daa` |

The v13 output is a headerless 4 MiB image. Its SHA-256 is
`461290feac2c13846a50b30bf8b69a744a8f0f7b8aca9c5421d1413b619455ae`.
The v17 output is also a headerless 4 MiB image; its SNES checksum is `0DEB`.

The public patcher accepts the verified original in headerless or 512-byte
headered form, plus v12–v19 releases. The Python patcher validates original and v12–v15 inputs through v16, then
through v17, v18 and v19 before applying the v19-to-v20 increment; v19 inputs receive that increment directly.
The separate full original-to-v20 BPS patch is available for graphical patchers. This records the
published upgrade path and does not package a ROM or private build material.

## Reusable lessons

- Body graphics, portraits, select icons, effects and backgrounds have separate
  resource paths. Replacing one does not automatically replace the others.
- Sprite DMA reads wrap within a 64 KiB bank. Relocate complete packets rather
  than placing them across a bank boundary.
- Projectile and independently animated effect loads must survive body
  repacking; ordinary body-pose tests do not exercise them all.
- Stage allocation must account for all 27 scenes, including map and bonuses,
  rather than only twelve battle stages.
- The shared portrait cache and temporary map buffers need explicit ownership.
  V12 uses 52,064 cache bytes, leaving 928 bytes before the relocated buffers.
- A flat stage map can be torn by original per-scanline scrolling. Inspect
  each rendered layer through a real camera sweep.

## V13 scrolling change

Stage 11's handler begins at file offset `0x1E215`. The cage is BG1 and the
room is BG2. The previous code selects different table positions for the
upper/lower wall. V13 changes:

| File offset | Before | After | Purpose |
| --- | --- | --- | --- |
| `0x1E21F` | `20` | `00` | Align the wall bands' table selection |
| `0x1E228` | `04` | `24` | Keep the subsequent cage lookup at `base + $24` |

The patcher checks the exact input hash and local handler bytes. Only stage
11 dispatches to this handler. The original perspective progression remains;
the room floor follows the corrected wall anchor.

## Public package boundaries

BPS patches encode a transformation, not a stand-alone game. Their source
copy operations can refer to original bytes at another location instead of
embedding those relocated resources as fresh literal data. This reduces
unnecessary redistribution but is not a copyright clearance mechanism.

The portable patcher implements the published
[BPS specification](https://github.com/Alcaro/Flips/blob/master/bps_spec.md).
The build process uses [Floating IPS](https://github.com/Alcaro/Flips);
its program source and binaries are not bundled here.
