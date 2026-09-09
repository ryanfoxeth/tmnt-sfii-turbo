# Verification of the game build

## V21 — 2026-09-09

Tested SHA-256: `27bab79c6cf21c284f9aa52d396088cdc8f1d8bd7983683d1e51e1a826dc8671`;
SNES checksum: `1913`.

- Bold purple Don and orange Mikey use the Leo/Raph alternate costumes in Normal
  and Turbo. Battle HUD and VS winner labels follow the costume. Select/VS bitmap
  captions and aggregate/static names remain LEO/RAPH.
- Only 425 ROM bytes change: palette words, display/palette-loader hooks and
  checksum. All sprite graphics, OAM/DMA, stage resources, moves and hitboxes
  remain exact. Native actor costume state is preserved.
- Ten matched controller routes cover both modes, primary/alternate costumes,
  swapped sides and same-slot mirrors. All 7,200 combat frames have identical
  fighter-state bytes to v20; all ten initial select screenshots are pixel-exact.
- Six two-KO VS routes confirm DON/MIKEY winner banners on both sides and in
  mirror matches. Arcade losses confirm alternate defeated/continue portraits
  for Normal Don player 1 and Turbo Mikey player 2. Health fixtures are logged;
  combat delivers the actual KOs.
- A 45,000-frame Arcade run completes all twelve stages, 24 KOs and three bonuses.
  KO frame/stage/opponent timing matches v20. Bonus scenery and objects were
  visually checked; whole-campaign rendered-frame identity is not claimed.
- Both BPS patches round-trip exactly. Ten actual CLI inputs (original and
  v12–v20) produce the verified target. Current v21 rejects without creating an
  output. Header normalization uses a synthetic header over the actual original
  payload because the pinned headered original was unavailable.
- Eighteen public tests and the 68-file public-tree audit pass. ROMs and private
  emulator states are excluded from this repository.

Representative emulator coverage, not original-hardware certification. Previous
Super Shredder walking004/005 gaps, turtle idle polish, voices, biography stats
and endings remain separate.

## V20 — 2026-09-09

Tested SHA-256: `69a71550ed6e9badfd4f2b277b4668b575f7d450ab250cd40604c12ea6dc6fbb`.

- Slash’s new scrapyard passes Normal/Turbo camera sweeps, 1,800 idle frames and
  native KO/outcome checks. The foreground fence stays stable.
- Leatherhead’s night palette and navy sky persist through Normal/Turbo KOs.
  Original background graphics and animation lists remain unchanged.
- Sixteen matched Casey routes cover both player sides, projectile speeds,
  blocking, collision and Flash Kick. Actor/OAM/health traces match v19;
  112 sampled images differ only within projectile bounds. Flash Kick is exact.
- A 45,000-frame Arcade route covers all twelve battle stages, 24 KOs and all
  three bonuses. The select screen matches v19. Bonus graphics were reviewed
  before and during destruction; their shared source data remains unchanged.
- Both BPS patches round-trip exactly. Nine actual CLI inputs (original and
  v12–v19) produce the exact v20 hash. Header stripping is tested with synthetic
  fixtures; the pinned physical headered source was unavailable for this run.
- The current release is rejected without output. Patch hash/CRC, revision and
  no-overwrite checks remain. The public tree excludes ROMs and save states.

Stage/KO checks use recorded pre-KO health fixtures; the campaign is not claimed
frame-identical to v19. This is emulator coverage, not original-hardware
certification. Super Shredder walking poses 004/005, turtle idle polish, most
voices, biography stats and endings remain separate work.

## V19 — 2026-09-09

Tested SHA-256: `a1cbd12ab115b81cfd7e970f4e331329715d0168ed0edb2c62a67c8ae5f7aec1`.

- Scope is Splinter's standing orientation only: logical poses 000–011, with
  366 changed bytes total (362 OAM x/HFLIP bytes plus four checksum bytes).
  Source tiles, DMA definitions, animation, palettes, allocation, game code,
  stages, effects and all other fighter OAM payloads remain byte-exact.
- Turbo and Normal controller traces cover 578 frames in both ports. Gameplay
  state traces match the v18 base exactly; Turbo also matches the exact pose-ID
  sequence, and both players face inward in standing and transition captures.
- Two Splinter real-KO outcome routes pass, with transitions and visual review:
  Turbo player-1 win and Normal player-2 loss.
- Full Arcade covers 45,000 frames, all 15 scenes, 24 knockouts and all three
  bonus stages. The fresh v18 base reproduces the historical timeline, while
  v19's late CPU campaign timing diverges first at Rocksteady KO17. Both builds
  complete the campaign and all 24 KOs; no whole-campaign frame-identity claim
  is made.
- Public BPS round-trips and the hash-pinned patcher checks cover the original,
  verified headered original, v12 through v18 inputs and current-v19 rejection.
  No ROM, save state or private build material is included.

This is representative emulator coverage, not original-hardware certification.
The open Super Shredder walking-pose waist gap 004/005 and unrelated turtle
idle polish remain outside v19.

## V18 — 2026-09-08

Tested SHA-256: `0e1e06361f4b21cddf425adb8b9fb072157cb32db1609aef609bcec7cadd7c20`.

- Four Super Shredder source poses receive 192 newly opaque waist pixels. All
  original opaque native palette indices and other fighter-9 packets are exact.
- Four 1,728-frame controller replays match v17 gameplay state and OAM in Normal/
  Turbo, both player sides. An additional replay uses a different stage.
- All 24 Normal/Turbo icon decodes match their expected repaired or preserved
  pixels. Six live Arcade/VS grids and four real-KO outcome paths were reviewed.
- Full Arcade: 45,000 frames, all twelve stages, 24 KOs and all three bonuses.
  Events and KO timing match v17. All 16 bonus captures are unchanged; 228 of
  251 campaign captures are identical. The other 23 change only intended icons
  (including the floating Arcade-map icon) or Super Shredder's waist.
- Public distribution: 14 unit tests, eight real CLI input round-trips and
  both new BPS round-trips pass. The 60-file public tree is allowlisted; patches
  are hash-pinned and no ROM or emulator state is included.
- The disjoint component merge reproduces the exact final hash; all 27 scene
  resource sets, other fighters, large portraits, palettes and game code remain
  exact. No new graphics allocation is required.

Controller replays use no state or RAM shortcuts. Outcome/campaign traversal
uses logged health fixtures and actual game-generated KOs. The source seam
scan covers 61 importable masters; it is not every animation combination.
This is representative emulator coverage, not original-hardware certification.

At idle transitions, previous OAM plus current VRAM matches the displayed
frame's sprite colors exactly; a current/current dump can mix snapshot phases.
Framebuffer correlation ruled out an apparent DMA tear. Native round-trip
success alone had also missed malformed source transparency.

## V17 — 2026-09-08

Tested target SHA-256:
`f0cf0064765bef202e75d5c7a664ff9406cfdba6e55bbaad16813d7d8ccd9daa`.

| Check | Result |
| --- | --- |
| Leatherhead and Slash fixed-scale review | All 85 Leatherhead and 104 Slash body poses reviewed; 29 Leatherhead and 69 Slash source corrections verified |
| Other-fighter inventory | 1,136 OAM entries across the other ten fighters recorded, including partial, effect and unmapped-tail cases; this is not exhaustive live coverage |
| Normal/Turbo combat | 19 Leatherhead and 18 Slash controller checks pass in each mode, with both player sides covered |
| Select, VS and battle UI | 24 cold-boot captures pass across Normal/Turbo and both sides |
| Outcome routes | Eight cold-boot win/loss/continue routes pass; health-only shortcuts are logged and real-KO transitions are checked |
| Full Arcade | 45,000 frames, all twelve fighting stages, 24 KOs and all three bonus stages pass; health-only shortcuts are logged |
| Visual review | Final fixed-zoom and live review passes; all twelve large neutral/defeated portraits remain v16-exact |
| Public distribution | Twelve unit tests, seven real CLI input round-trips and both new BPS round-trips pass; tracked files are allowlisted and patches are hash-pinned |
| Component merge | Repeating the recorded component merge produced the same final hash; this does not claim a second full source-pipeline rebuild |

The other-ten-fighter OAM inventory includes intentional partials and entries
that are not a complete live animation/VRAM exercise. Save states do not cross
ROM versions. These representative emulator checks do not certify original
hardware or every two-character interaction. Turtle idle polish, the separate
Super Shredder body concerns, voices, endings and credits remain outside this
release.

## V16 — 2026-09-08

Tested target SHA-256:
`389c89355c252d3ad5e8dca5f73e66ad23a27254e094e30ce310b1a37371de71`.

| Check | Result |
| --- | --- |
| Both new body components, Normal/Turbo mirror matches | Controller suites pass on both player sides; idle, attacks, damage and special-move inputs covered |
| Slash live idle graphics | Complete packets match both player VRAM banks after fixing the source-cell crop |
| Fighter DMA banking | All 12 fighter tables stay within 64 KiB source banks |
| Shared resource audit | All 27 scene streams and ten unrelated fighters' packets/palettes/portraits preserved |
| Final VS review | 24 select, full-portrait and battle captures across both fighters, sides and modes |
| Final win/loss/continue routes | Eight cold boots, two real HP-to-FF knockouts per route; independent portraits and quotes reviewed |
| Portrait cache | 55,936 bytes; complete cache matches before selection, 1,152 bytes of buffer slack |
| Gray defeated icons | Both new icons reviewed on actual Arcade maps |
| Mixed Arcade | 45,000 frames, all twelve fighting stages, 24 KOs and all three bonus stages |
| Bonus/results review | 16 bonus captures plus early/late KOs through age 600 reviewed |
| Rebuild and distribution | Source rebuild and both private IPS round-trips exact; five public BPS source/target round-trips exact |

The Arcade/outcome traversals use logged health-only shortcuts; body combat
checks use controller input. Larger portrait loading changes cold-boot timing
and later random-state-dependent traces. Exact v15 campaign timing is not
claimed. The failing strict historical battle comparison is retained in the
private evidence rather than reported as passing.

Slash's tested scanline maximum is 32 tile columns. Leatherhead's rolling
case reaches the original Blanka peak of 42; it is not universally below
hardware limits. These are representative emulator checks, not exhaustive
frame-combination or original-hardware certification. The separate Super
Shredder body report and turtle idle polish remain open.

## Historical v13 checks

These checks were run locally against the exact v13 SHA-256 documented in
the release history. The public repository contains no ROMs or emulator save states.

| Check | Result |
| --- | --- |
| Nine camera positions, room layer isolated | Both wall bands match one horizontal translation exactly; zero separation |
| Same positions in v12 | Up to 18 pixels of separation |
| Full camera sweep | Cage-only rendering matches v12 |
| Three 640-frame layer passes | Fighter RAM and OAM match v12 throughout |
| Wall-jump/flying-attack sequences, both player sides | 767 frames per side; cage pixels, fighter RAM and OAM match v12 |
| Full Arcade route | 45,000 frames, all twelve battle stages, 24 KOs |
| Arcade timing | Scene events and KO timing match v12 |
| Captures in that route | 230 of 244 match v12; all 14 changed captures are on Shredder's stage |
| Bonus scenes | All 16 sampled frames across all three bonuses match v12 |

The camera and wall-jump checks use controller inputs only. The Arcade test
uses documented health-only shortcuts to traverse the game. No source ROM
or emulator-core modifications were used for these tests.

These are representative emulator checks, not exhaustive animation,
all-emulator or original-hardware validation. The README lists known art
limitations. Public CI tests the patch parser with synthetic inputs; it
does not secretly download a game ROM or repeat gameplay tests.

## Day 3 video follow-up — 2026-09-08

Fresh controller-only v18 footage exposes a remaining Super Shredder waist
separation around 3.2 seconds into the idle/walk review route. Native pose
004/005 inspection confirms the separation is in authored pose data. The
v18 repair covered poses 000–003; it did not repair 004/005. The same defect
is present in the source capture, so it is not a video-compositor artifact.
No ROM or patch bytes changed in this documentation follow-up. The earlier
regression checks establish the documented preservation and route coverage,
not that every visible pose has finished art.
