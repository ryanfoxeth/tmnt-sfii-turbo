# New reskin playbook

Use this workflow when continuing TMNT SFII Turbo or beginning a similar
reskin. It is deliberately split in two: continuing the same engine can reuse
evidence after checking its version and ownership; a new game requires fresh
reverse engineering. Do not invent a Mortal Kombat mapping or treat the TMNT
fighter map as a template for one.

## First decision: same engine or a new game?

| Situation | Start from | What may transfer | What must be rediscovered |
| --- | --- | --- | --- |
| TMNT SFII Turbo follow-up | v29 public patch/release facts and the matching private v29 build evidence | Existing slot identities, cumulative ledgers, known graphics/UI/stage contracts, current QA fixtures | Any resource touched by the change; final candidate hash; every affected reader and runtime path |
| Another reskin of the same exact SFII Europe/PAL 1.0 engine | A clean hash-pinned original plus a new project/ledger | Method, source/export discipline, and the need to preserve original moves/hitboxes when that is the intended scope | New character mapping, visual approval, all allocations/consumers, art fit, and all QA evidence |
| Another ROM or engine | A pristine supplied ROM and a new project | Only the investigation method and evidence standard | Codec, pointers, entity model, palettes, compression, upload path, RAM/VRAM, text/audio, stage/bonus/ending consumers, hardware budgets, and distribution rules |

For the first two cases, validate the source revision and write down the
SHA-256 before opening a save state or running an importer. The public v29
patch target and supported input identities are in [release.json](../../release.json).
The current patcher is the public delivery entrypoint, not a graphics editor:

```bash
python3 apply_patch.py "/path/to/original.smc" --out "TMNT-SFII-v29.sfc"
```

It validates the accepted source/hash chain and refuses to overwrite an
existing output. Its patch behavior and public boundaries are described in
[README](../../README.md). A future release must produce a new, hash-bound
candidate rather than overwrite that record.

## Phase 0: define scope and a durable evidence folder

Write a one-page scope before generating art. Include: source ROM/revision and
hash; intended engine contract (visual-only or a requested mechanic change);
proposed character mapping; art direction; stage/portrait/text/audio scope;
distribution target; and acceptance criteria. For a same-engine visual reskin,
say plainly that the original moves, hitboxes, AI, timing, and collision stay
in place. A new game has no such presumption.

Create a versioned private work directory outside this public repository. Give
each candidate a machine-readable manifest containing the input hash, output
hash, changed ranges by owner, generated-art/source hashes, tool revision,
tests, captures, exceptions, and delivery state. Preserve failed and
experimental candidates separately. Do not publish ROMs, private source media,
save states, or extracted base-game assets here.

The private companion is `ryanfoxeth/sf2-reskin-workbench`, with a
full private Dropbox workspace archive. Treat that archive as a relocation
package: unpack it so its recorded **relative** workspace paths reconstruct,
read its manifest, then validate the source/hash prerequisites before executing
anything. It preserves art/source material and native evidence; it is not a
generic one-command build-from-source system. Historical tools are hash-pinned
and subsystem-specific, and several require prior component outputs and
cumulative allocation ledgers.

## Phase 1: reversible discovery before art

Make a minimal inventory and prove each claim with an unchanged round trip or
a small live experiment.

1. Establish whether data is raw, tiled, planar, compressed, banked, pointer
   indexed, or generated at runtime. Record dimensions, transparency,
   tile order, palette format, alignment, compression size, and pointer form.
2. Select one representative fighter and map idle, locomotion, attack,
   hit/knockdown, a detached effect, icon, neutral portrait, defeated/continue
   portrait, names, and a stage. Recover OAM/OBJ-or-equivalent descriptors,
   animation scripts, upload packets, source and destination addresses, and
   shared consumers.
3. Map runtime boundaries: ROM allocation, decompression target, scratch RAM,
   VRAM/tile destination, palette/CGRAM-equivalent data, source-bank/page
   restriction, and scanline/object budget. Validate both player sides or
   equivalent load paths.
4. Map every presentation and world consumer: select, VS, HUD, winners,
   records, continue/map, all stages, bonus stages, destructible/late-state
   objects, endings, credits, title/menu, and audio where it is in scope.
5. Build an ownership ledger. A byte or tile is reusable only after every live
   reader and prior reservation has been identified; zero fill is not proof.

Only then create a one-character native proof: idle, movement, attack,
hit/knockdown, special effect, icon, portrait states, and needed text. Inspect
it live at native scale. A PNG round trip and a contact sheet cannot establish
correct runtime registration, loading, or silhouette.

## Phase 2: art system and import discipline

Set a shared style sheet before batch work: canvas/scale, anchor and ground
line, palette roles, outline treatment, lighting direction, pose-family
proportions, icon crop rule, portrait orientation, and background policy.
Keep source provenance and editable masters privately with deterministic
conversion inputs.

For each body family, extract the whole connected figure before measuring.
Cell labels, neighboring poses, transparent continuation cells, and cross-cell
poses are frequent traps. Register to the original mesh and preserve intended
partials, flips, overlap, crouches, rolls, falls, and effect silhouettes.
Quantizing a beautiful master does not make it fit an original OAM layout.

Integrate sequentially from an immutable baseline. Each component reports its
owned writes and input/output hashes. Merge only after checking that write
ranges are disjoint except for explicitly shared, reviewed fields such as a
checksum. Never bypass a historical builder's input guard merely to compose a
new candidate.

For same-engine SFII work, the private sibling checkout contains useful
version-bound tools. The following `--help` interfaces were verified; they are
examples to inspect and adapt, never generic commands for a different game:

```text
tools/roster_body_pipeline.py {export,register,import} \
  [--fighter april|bebop|casey|splinter|rocksteady|super-shredder|krang|all] \
  [--rom ROM] [--out OUT] [--masters MASTERS] [--sheet SHEET] \
  [--layout LAYOUT] [--pose-ids ID[,ID...]]
tools/roster_body_repack_generic.py --fighter FIGHTER \
  [--base BASE] [--expansion-start START] [--expansion-end END] \
  [--expansion-range START:END]... [--out OUT]
tools/roster_portrait.py --rom ROM --capture CAPTURE --out OUT
tools/compile_roster_icon.py --source SOURCE --palette PALETTE --out OUT
```

The body pipeline's fighter list is historical and excludes Leatherhead/Slash;
it is not proof that the current roster is fully handled by one generic
importer. `roster_body_repack_generic.py` also has a narrower historical
fighter set. Read its source, the active build wrapper, and the current ledger
before use. The public repository retains selected v16/v17 art metadata but
not the private importer workspace. The private workbench/archive
supplies that historical material after its manifest and reconstructed relative
paths are verified.

## Phase 3: presentation and stage completion

Finish every distinct presentation resource rather than producing one generic
portrait. Test color and gray icons separately; inspect their backgrounds,
borders, opaque interior, padding, and full height. Test neutral, defeated,
continue, and map/defeat portraits on both sides. Record which source
orientation the renderer expects. Treat every name system as a separate
reader with a separate encoding and width budget.

For a stage, write an explicit policy:

* **Static scenery:** retire every obsolete decorative tile/map/palette/object
  update that would reveal old art, while retaining scrolling, mechanics, and
  requested objects.
* **Animated scenery:** supply each later frame, map write, palette cycle,
  object update, and destination deliberately.

In either case, inventory ordinary stages, bonuses, endings, and any shared
loader/resource streams before relocating assets. Test camera extremes,
stationary time, round transitions, initial/damaged/destroyed objects, and
late results. The detailed SFII-specific implementation lessons are in
[Graphics, stages, UI, and QA handoff](GRAPHICS-STAGES-UI.md).

## Phase 4: release-quality QA

Run focused tests early, then a candidate-hash-bound integration pass.

1. For each changed fighter: Normal and Turbo (when applicable), both sides,
   all affected palettes/costumes, repeated special moves/effects, damage,
   throw, KO, win/loss, and relevant UI outcomes.
2. For each changed UI surface: select, VS, HUD left/right, winner, records,
   continue/map and both portrait/icon variants.
3. For each changed stage: initial and delayed states, camera endpoints,
   late KO/results, ordinary and special mechanics, every mode, plus any
   matching bonus/ending consumer.
4. Run complete progression: all ordinary stages, bonuses, endings/credits,
   title/menu return. Use controller input for behavior claimed as live
   gameplay; label health/RAM shortcuts and do not elevate them to controller
   proof.
5. Compare matched control/candidate state traces, pixels, OAM/VRAM-or-
   equivalent data, and gameplay state. Separate known loading-phase shifts
   from actual regressions. Review the framebuffer as well as raw memory.
6. Rebuild independently; verify output hash, patch round trip, public-tree
   allowlist, and test suite against the exact release candidate.

The public v29 record reports 38 tests, a 92-file public audit, and 19 patcher
input routes. It also reports a final Slash Turbo Arcade route through all 12
stages, three bonuses, endings/credits, and title/menu. This is useful evidence
for the released TMNT patch only; it is not a template claim for a different
ROM or a physical-hardware certificate.

## When continuing TMNT SFII Turbo

Start from v29 and read [README](../../README.md),
[technical notes](../technical-notes.md), [verification](../verification.md),
and the new graphics handoff before opening the private workspace. The newest
private status is v29, so older v17 next-game notes are historical context,
not the terminal baseline. Preserve current work that is explicitly outside a
new request: the original soundtrack (the Music Lab is paused), accepted voice
work and non-vocal effects, current endings, and repaired fire-effect
semantics. Turtle idle polish remains open.

Before modifying a graphics component, find the current private build guide,
allocation ledger, and candidate receipt for that component. Build from its
hash-pinned predecessor, keep one emulator/build/render at a time, and use a
fresh process per route. Do not use a v29 save state against another candidate.

## Sources, certainty, and exclusions

The public sources for final release facts are [README](../../README.md),
[release.json](../../release.json), [technical notes](../technical-notes.md),
and [verification](../verification.md). The private-workspace descriptions and
tool interfaces in this playbook were checked on 2026-09-12 against current
project guides and `--help` output. They are marked historical/version-bound:
the planned `sf2-reskin-workbench`/Dropbox archive preserves the workspace but
does not turn its old build scripts into a generic from-source pipeline.

No character mapping is supplied for a future Mortal Kombat reskin or any
other game. That is an undecided creative and technical scope choice. No ROM,
binary source media, private capture, or private absolute filesystem location
is included or required by these public documents.
