# TMNT × Street Fighter II Turbo

A fan-made visual overhaul of **Street Fighter II Turbo for SNES**: twelve TMNT
characters, ten custom stages, and the original fighting moves underneath.
Built with Ryan's creative direction and Codex/Astra assistance on Linux.

**Current version: v18.** This repository distributes patches and tools.
You supply the matching original game; no complete game ROM is included.

![Repaired select grid](assets/select-v18.png)

## Play

1. Download this repository using **Code → Download ZIP**, then extract it.
2. Supply your own lawfully obtained **Street Fighter II Turbo, Europe/PAL,
   version 1.0** ROM. US, Japanese and other revisions are not supported.
3. With Python 3.9 or newer, run:

   ```bash
   python3 apply_patch.py "/path/to/original.smc" --out "TMNT-SFII-v18.sfc"
   ```

   On Windows, use `py -3` in place of `python3`.

4. Open the generated file in an SNES emulator. Start from a fresh boot;
   an older save state may retain outdated graphics or scrolling data.

The patcher runs locally on Linux, macOS or Windows. It checks the input
revision, patch checksums and final output hash, and refuses to overwrite
an existing file. It accepts the exact original (including the verified
512-byte-headered form) and v12 through v17 releases. Older releases are
validated through the v16 and v17 intermediates; v17 uses its direct v18 increment.
It never downloads a ROM or sends your file anywhere.

For a graphical patcher, the `.bps` files in `patches/` work with
[Floating IPS](https://github.com/Alcaro/Flips). The full patch expects a
**headerless** original; the included Python patcher also handles the
verified original with its 512-byte copier header.

## Roster

| Original fighter | Replacement |
| --- | --- |
| Ryu | Leonardo / Leo |
| Ken | Raphael / Raph |
| Chun-Li | April |
| E. Honda | Bebop |
| Guile | Casey Jones |
| Dhalsim | Splinter |
| Balrog, the boxer | Rocksteady |
| Vega, the claw fighter | Shredder |
| Sagat | Super Shredder |
| M. Bison, the dictator | Krang's android body |
| Blanka | Leatherhead |
| Zangief | Slash |

Leatherhead and Slash use their original-cartoon designs and retain Blanka's
and Zangief's moves and stages. The design references the original
TMNT cartoon and the NES/SNES games. Leonardo has a tight Japanese night
backstreet; Shredder, Super Shredder and Krang have distinct Technodrome rooms.
The original cage and wall-jump mechanics remain on Shredder's stage. V18
includes the v14 icon-framing and v15 background-animation corrections.

## V18 cleanup

Seven select icons now use the full bust height, removing the empty bands
while preserving gray borders and opaque backgrounds. Super Shredder's four
affected waist poses are repaired without changing moves or animation timing.

![Super Shredder before and after](assets/cleanup-v18.png)

## What is included

- Full original-to-v18 and direct v17-to-v18 BPS patches, plus patcher support
  for original/headered and v12–v17 inputs.
- Earlier BPS patches, including the historical v13 patches, remain available.
- A portable, hash-checked Python patcher and format-level tests.
- Standalone source for v13's scrolling repair and v15's stage-animation fix.
- Retained artwork masters and layout metadata in [art/v16](art/v16/README.md),
  plus the v17 [geometry review](art/v17/README.md).
- [Release history](docs/releases.md), [technical notes](docs/technical-notes.md),
  and [contribution guidance](CONTRIBUTING.md).

This is the public distribution and patch-tool repository. The complete
historical art-generation workspace and emulator development environment
are not packaged here. The v13 and v15 fix sources reproduce their respective
increments; the full playable reskin is reproducible by applying the full
patch to the verified original.

## Current limits

Turtle idle animation still needs polish. Endings and credits are mostly
original, and their story artwork still needs a later pass. Most replacement
fighters retain their original voices; Shredder has the earlier lowered
voice treatment. Some original world-map/biography identity fields remain.
V18 repairs the transparent belt/waist pixels confirmed in Super Shredder's
poses 000–003. A subsequent Day 3 video review found that walking poses
004/005 still have a horizontal waist separation; those two poses remain
open in the current v18 patch. This is a work in progress.

The v18 regression run replays Super Shredder's gameplay in Normal and Turbo
on both sides, checks six select-grid routes and four outcome routes, then
all twelve fighting stages, 24 knockouts and all three bonus stages. See [verification](docs/verification.md) for the
scope and limits; this is not an original-hardware certification.

## Rights and distribution

This is an unofficial fan project, not affiliated with or endorsed by the
Street Fighter or Teenage Mutant Ninja Turtles rights holders. Those
characters, names, original game material and trademarks remain the property
of their respective owners.

A patch avoids distributing the complete base game, but it can still contain
copyrighted or derivative material. Patch format and noncommercial status
do **not** establish permission or immunity from takedowns. No license to
third-party franchise or game content is granted here. The original Python
tooling is offered under the [MIT license](LICENSE); that license excludes
the patches, game artwork, screenshots and third-party content.

Background: [U.S. Copyright Office on derivative works](https://www.copyright.gov/eco/help-limitation.html)
and [GitHub's DMCA policy](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy).
Please do not upload ROMs, emulator save states, extracted original game
assets or ROM-download links in issues, pull requests or releases.
