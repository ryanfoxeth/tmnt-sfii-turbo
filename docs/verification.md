# Verification of the game build

These checks were run locally against the exact v13 SHA-256 documented in
the README. The public repository contains no ROMs or emulator save states.

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
