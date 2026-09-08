# Verification of the game build

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
