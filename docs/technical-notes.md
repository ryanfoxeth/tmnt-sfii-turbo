# Technical notes

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

The v13 output is a headerless 4 MiB image. Its SHA-256 is
`461290feac2c13846a50b30bf8b69a744a8f0f7b8aca9c5421d1413b619455ae`.

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
