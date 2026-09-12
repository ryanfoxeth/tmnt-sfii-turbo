# Graphics, stages, UI, and QA handoff

This guide records the visual-reskin method that produced TMNT SFII Turbo
v29. It is a map for a future maintainer, not a claim that the private build
workspace is a portable editor. The published release is the patch set at
commit `15593e4`; its target is the verified Europe/PAL 1.0 game and its final
4 MiB output hash is recorded in [the release manifest](../../release.json).

## Scope and fixed engine contract

TMNT SFII Turbo is a **same-engine roster reskin**. Each of the 12 original
fighter slots has new presentation, while the original moves, timing,
hitboxes, AI, collision, and slot identity remain. This is why a character
such as Slash still plays through Zangief's engine slot. It is not evidence
that a new roster can be inserted into this ROM, nor that any of its offsets,
formats, budgets, or RAM/VRAM behavior transfer to another game.

V29 preserves the v28 graphics/state: twelve fighter presentations, eleven
changed backgrounds (including Leatherhead's retained riverside at night),
costume-aware turtle UI, fourteen illustrated ending packages with small
environmental loops, and the repaired fire effects. The current public
limits and the measured release coverage are stated in [README](../../README.md)
and [verification notes](../verification.md). Public technical ownership
facts live in [technical notes](../technical-notes.md).

## What must be mapped before visual edits

Treat the following as an ownership graph, not a list of convenient files.
For every candidate change, identify every edge that reaches it and every
other consumer that shares it.

| Surface | Required ownership record | Failure if skipped |
| --- | --- | --- |
| Fighter body | pose/animation ID; each graphics packet; OAM/OBJ mesh; palette; DMA/upload descriptor; flip/inheritance rules; attachments and effects | A correct still can lose limbs, read another bank, overload scanlines, or overwrite a projectile/flame. |
| Presentation UI | color icon; gray icon; icon background and border; neutral, defeated, continue, and map/defeat portraits; all name encodings | Select can look right while the VS, winner, continuation, map, or opposite side remains wrong. |
| Stage | initial tiles, maps and palettes; layer ownership; later map/tile/palette/object writes; camera/scroll handler; damaged/destructible variants; bonus/ending loader consumers | New battle art can corrupt a bonus room or reveal original scenery after time/camera movement. |
| Runtime memory | ROM range, decompression output, scratch RAM, VRAM destination, tile indices, DMA source-bank boundary, OAM/scanline cost | A binary patch may apply but fail only on P2, a special move, or a late round. |

Zero-filled data is never sufficient evidence that a range is free. Follow
live references, previous allocation ledgers, and all readers first. In this
project the cumulative ledgers are private build artifacts; check the current
one plus earlier ledgers before extending a private build. The public record
documents several concrete contracts: the portrait cache and temporary-map
buffers, ending VRAM/palette ownership, the 64 KiB DMA source-bank limit, and
the v20 stage/bonus collision. See [technical notes](../technical-notes.md).

## Fighter graphics: source to native frame

1. Export a representative native body set and reconstruct the entire
   allocated footprint: transparent cells, hidden pieces, partials, flips,
   inherited graphics, and separate effect tails. Make an unchanged
   export/import round trip before integrating replacement art.
2. Create a style sheet before a batch: native scale, outline weight, allowed
   palette roles, lighting direction, anchor/ground line, and which poses may
   deliberately be short, wide, prone, or cross source-sheet cells. Keep
   prompt/provenance and editable masters out of this public distribution.
3. Measure the connected figure, not a nominal contact-sheet cell. V17 found
   labels and adjacent Slash drawings expanded a cell's bounds and shrank the
   actual body on import. Blank continuation cells can require recovering the
   predecessor drawing; v17 poses 099/100 deliberately share one recovered
   cross-cell kneeling figure.
4. Quantize to the proven palette and register art to the original mesh. Do
   not normalize crouches, rolls, falls, or effects to standing proportions.
   Preserve intentional overlap where native OAM uses it.
5. Audit every changed DMA packet and descriptor in live execution. A packet
   may not cross a 64 KiB SNES source bank. In the v17 final measurement Slash
   consumed 9,441 of 9,445 owned OAM bytes; that number is a documented local
   constraint, not a general budget to reuse.
6. Run the original special moves, repeated effects, throws, hit/knockdown,
   win/loss states, both player sides, and Normal/Turbo. Compare a matched
   control state where a graphics loading phase can differ from a real
   gameplay regression.

### Effect and silhouette traps

Body importers must preserve effects that are not ordinary body poses. The
v28 repair is the clearest counterexample: Slash pose 084 and Leatherhead pose
089 are burn silhouettes whose original semantics require **empty DMA plus
their original OAM**. Treating them as body art uploaded over retained burn
tiles destroyed the upper silhouette. Splinter's flame poses 111–117 also
required their effect OAM layouts, not merely restored flame CHR/DMA. The
repair changed existing OAM/DMA tables only; it did not add body art or a new
allocation. Both directions and all seven flame poses received fresh
controller coverage. This is tested behavior, not a blanket assurance for
every effect in another ROM.

Use the same rule for projectiles: Casey's hockey stick belongs to release
pose 037, not a protected whole-body pose guessed from a still. Its two
auxiliary loads were omitted by an earlier repack; full live tracing located
the P1 destinations EC00/EE00 and P2 destinations FC00/FE00. Test every
detached effect independently from body-pose checks.

## Icons, portraits, and text

Icons and portraits are independent resource paths. Do not crop one master
and assume every UI consumer uses it.

* Color and gray select icons use distinct assets, palettes, and loading
  paths. The small-icon convention is an opaque 19×30 interior inside a gray
  border, with transparent allocation padding. Inspect the full box at native
  size: a face-coverage test missed the blank bands that V18/V17 corrected.
* Neutral and defeated/continue portraits may be separately compressed.
  In this game neutral portraits are stored facing right and the renderer
  mirrors the right-side screen placement; defeated resources have their own
  inward-facing convention. Verify select crop, full VS, winner/loss,
  continue/map result, both sides, and each available costume palette.
* Each label system has its own encoding, tile/caption budget and semantics:
  select, VS, HUD left/right, winner, records, biography, and continue/map.
  V21/V22's Don/Mikey work demonstrates that a costume-aware caption does not
  make every static label costume-aware. Retain a table of field, reader,
  max width, and tested state.

The private workspace has useful **historical, version-bound** entrypoints;
they are not packaged in this repository or general importers:

```text
tools/roster_portrait.py --rom ROM --capture CAPTURE --out OUT
tools/compile_roster_icon.py --source SOURCE --palette PALETTE --out OUT
tools/verify_portrait_states.py
```

The first two command interfaces were checked with `--help`. The verifier has
no stable public CLI contract recorded here, so inspect its source and the
version-specific report before invoking it. The retained public art metadata
and its limitations are in [art/v16](../../art/v16/README.md) and
[art/v17](../../art/v17/README.md).

## Stages: maps, animation, scroll, and bonuses

A stage is not a screenshot. It consists of initial layers plus later updates
to tiles, maps, palettes, objects, and sometimes camera/scroll logic. Decide
the policy deliberately.

For a static reskin, retire obsolete decorative map/palette/object updates
while retaining gameplay objects and requested scrolling. V15 redirected 87
obsolete animation-list entries to an existing empty list for the replaced
rooms; it did not blindly clear a VRAM range. The Shredder cage's mechanics and
scrolling remained live. For an animated reskin, replace every frame, list,
destination, and palette transition that can become visible. A static map
round trip does not prove either policy.

The v20 Slash stage demonstrates shared-resource risk. Its new battle-stage
loader is redirected, but Zangief's original compressed stream also serves
bonus scene 13, so that stream and its bonus loader remain exact. The result
was checked against all 27 scene layout graphs **and** all 27 loader/resource
streams. Leatherhead's night scene changes room-local backdrop/background
palettes while retaining stage maps, animation lists, fighter palettes, and
HUD palettes. These exact placements are SFII-specific; the transferable rule
is to inventory all consumers before relocation.

The historical stage-tools interfaces below were verified with `--help`:

```text
tools/stage_resources.py --rom ROM --captures CAPTURES --out OUT
tools/export_stage_layers.py CAPTURE OUT
tools/compile_technodrome_art.py --source SOURCE --out OUT \
  [--no-mirror] [--source-floor SOURCE_FLOOR] [--tile-budget TILE_BUDGET] \
  [--preserve-region x0,y0,x1,y1]
tools/technodrome_stage_layout.py --entries ENTRIES [--rom ROM] [--out OUT]
tools/technodrome_animation.py --entries ENTRIES
```

They describe old discovery/Technodrome workflows. They must not be pointed
at v29 and assumed cumulative; read their version guards, current allocation
ledger, and reports first. In particular, `package_stages_v20.py` was a
one-time draft stager and is not a cumulative release builder.

## QA matrix and evidence standard

Every evidence file must name the tested candidate hash, source/control hash,
emulator/core, route, input method, and permitted comparison masks. Never use
a state created by another ROM version. A RAM setup shortcut can accelerate a
fixture but must be logged and must not be presented as controller proof.

| Area | Minimum live coverage | Why |
| --- | --- | --- |
| Fighter | Normal and Turbo; P1 and P2; move/effect family; hit/throw/KO/win; selected alternate palettes/costumes | P2 VRAM banks, transformed effects, and outcome readers differ. |
| UI | select, VS, HUD on both sides, winner/loss, continue/map, records; all icon and portrait families | One screen rarely exercises all assets or name readers. |
| Stage | initial load; stationary time; camera extremes; round transition; late KO/results; each mode; stage-specific mechanics | Old lists or palettes can appear after a delay or at a camera edge. |
| Global consumers | every ordinary stage, all bonuses, endings/credits and return to title/menu | Shared streams can collide outside combat stages. |
| Regression | exact component merge/non-overlap audit, all resource consumers, patch round trip, public allowlist/tests | A visually successful patch can contain unreviewed bytes or package the wrong output. |

Tested release evidence includes the v29 fresh Slash Turbo Arcade route:
39,163 frames, 24 KOs, all 12 stages, all three bonuses, seven ending/credit
pages, and return to title/menu. Earlier graphics-stage release evidence
includes V15's camera/late-KO matrix and v20's 27-scene/loader audit. These
are emulator results; they are neither original-hardware certification nor an
exhaustive proof of every two-fighter VRAM combination.

Useful historical runner interfaces, checked with `--help`, are:

```text
tools/emulate.py ROM [--steps STEPS] [--out OUT] [--load-state LOAD_STATE]
tools/play.py ROM [--scale 1..6] [--mute] [--skip-intro] \
  [--load-state LOAD_STATE] [--no-audio] [--frames FRAMES] [--unthrottled] \
  [--screenshot SCREENSHOT]
tools/verify_roster_combat.py record ROM OUT --fighters ID [ID ...]
tools/verify_roster_combat.py compare CONTROL_DIR CANDIDATE_DIR OUT
```

`verify_roster_combat.py` records pose/state traces and visible scanline OBJ
pressure. Its own output explicitly says that the comparison flags added
worst-case pressure; it does not prove every scanline is within hardware
limits. Review framebuffers as well as OAM/VRAM dumps: captures from different
emulator phases can pair previous OAM with current VRAM and fabricate an
apparent DMA fault.

## Known gaps and source trail

This guide intentionally does not claim that private masters, source media,
ROMs, save states, emulator captures, allocation ledgers, or the full editor
are public. A separate private source/tool repository is
`ryanfoxeth/sf2-reskin-workbench`, accompanied by a full private Dropbox
workspace archive. When delivered, the archive must reconstruct the private
relative paths after relocation and include a manifest that names the source
revision and hashes. It is evidence and a recoverable workspace, not a generic
one-click from-source pipeline: historical builders have hash guards, narrow
fighter lists, and version-specific allocation assumptions. V29 remains
limited to its stated scope: turtle idle polish is open; the Music Lab
experiment is paused; short shared hurt sounds and April's KO voice remain
stock; ending motion is localized environmental animation.

Primary source trail: public [README](../../README.md),
[release manifest](../../release.json), [technical notes](../technical-notes.md),
[verification](../verification.md), and retained [v16](../../art/v16/README.md)
and [v17](../../art/v17/README.md) art records. Private-source facts in this
guide were checked against the current private `README-Replacements.md`,
`README-Stage-Animation-V15.md`, `README-Stages-Projectile-V20.md`,
`README-Consistency-V17.md`, `README-Fire-Voices-V28.md`, and the named tool
interfaces on 2026-09-12. Those private documents supersede the stale v17
next-game handoff for SFII status; their paths and historical commands are
references, not public dependencies.
