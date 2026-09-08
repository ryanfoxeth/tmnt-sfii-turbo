# Leatherhead and Slash artwork

These generated masters follow the original 1987 TMNT cartoon: turquoise
Leatherhead with his Cajun hat, vest and waders; olive Slash with a silver
metal mask, ochre chest and purple belt/spikes.

Each character folder contains generated pose sheets, separate intact and
defeated portrait drawings, generation prompts and native layout coordinates.
The reference manifest links to the design references; downloaded third-party
photographs and original-game export sheets are excluded. Local filesystem
paths have been removed from the public metadata. The original prompt text
and source files are retained privately.

These are working art sources, not sprites that can be pasted directly into
any ROM. Import requires foreground extraction, native registration,
16-color quantization, tile/OAM packing and allocation checks. In particular,
extract the entire generated cell before fitting it: cropping Slash to the
old Zangief source rectangle cut off limbs while still passing a static
round-trip check. Test the installed animation in an emulator.

V16 installs 85 Leatherhead body poses and 104 Slash body poses. Shared
auxiliary effects are preserved. Both characters also have small color/gray
icons, independent defeated portraits, display names and short quotes.
Leatherhead uses `LEATHER` in narrow caption/winner fields and `LEATHERHEAD`
in the HUD and records. Their original stages and fighting logic remain.

The complete historical importer/emulator workspace is not bundled in this
public distribution. The verified playable build is reproduced by applying
the BPS patch to the supported original or an exact previous release.
See the root README and technical notes for those contracts.

The repository's MIT license covers original code only. These franchise
characters, artwork and derivatives are excluded from that license.
