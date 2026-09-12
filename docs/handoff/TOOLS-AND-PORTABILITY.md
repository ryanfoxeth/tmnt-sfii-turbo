# Tools and portability handoff

This repository is the public distribution and patch-application project. The
private authored-code and documentation repository is
`ryanfoxeth/sf2-reskin-workbench`. The complete private Dropbox archive retains
art masters, source media, ROM work products, saves/states, diagnostics, and
the tools that created them. Do not place a commercial ROM, extracted ROM data,
third-party source media, private recordings, personal paths, or credentials in
this public repository; keep ROMs and source media out of the private code Git repo too.

## What the public project can reproduce

At commit `15593e41f69424b2aa205577d865cb41f1e0bdc6`, this project publishes
the v29 patch set. `python3 apply_patch.py` applies a selected BPS patch to a
user-supplied legal, pristine, headerless 2,621,440-byte Street Fighter II
Turbo input. The output v29 ROM expands to 4 MiB. The patcher also accepts the
verified original with a 512-byte copier header and v12 through v28 releases.
The application and test path is portable across supported Python 3 systems:
it uses the checked-in `bps.py`, standard-library Python, and the checked-in
patch files. Run `python3 -m unittest discover -s tests -v` after cloning.

That is a patch application path, not a source rebuild of the reskin. The
private build chain has not been demonstrated to rebuild v29 from an original
ROM alone on a clean machine. It begins with a hash-pinned private v28 output,
which is itself a derived ROM. Treat the public patch and its documented input
hash as the portable consumer artifact; retain the private lineage for editing.

## Verified v29 private build chain

Run these commands from the root of a restored private workbench, using its
venv interpreter when available. The commands use repository-relative paths.

```sh
python tools/add_actor_voices_v29.py
python tools/finish_private_voices_v29.py \
  --source work/all-voices-v29/actor-routing-r2/tmnt-roster-v29-actor-voice-candidate.sfc \
  --out work/all-voices-v29/combined-r2/voice-candidate.sfc
python tools/finish_voice_events_v29.py \
  --source work/all-voices-v29/combined-r2/voice-candidate.sfc \
  --out work/all-voices-v29/combined-r5/voice-candidate.sfc
```

The required base is `work/fire-fixes-v28/build-final/tmnt-roster-v28.sfc`,
SHA-256 `72d15ae80928b3ede4a94a3e58ff46a3ae93a9d786151b4e4f5f3ca26a4e2a3b`.
The expected final candidate and canonical v29 ROM SHA-256 is
`03e1060d04be410d93d7a87e6668b51e6189d99ba887c526404f2c113df9001a`.
The canonical copy is
`work/all-voices-v29/build-final/tmnt-roster-v29.sfc`. The final `combined-r5`
candidate is the only releasable candidate; intermediate routing directories
are retained as diagnostic evidence.

The scripts make strong byte-level assertions and import helpers across older
release tools. Keep the complete private `tools/` directory and all historic
`work/` content; copying only the three entry scripts is insufficient. The v29
chain also consumes selected BRR files in `work/all-voices-v29/audio/`.

## Runtime and tool groups

| Group | Role | Portability status |
| --- | --- | --- |
| Public `apply_patch.py`, `bps.py`, tests | Patch distribution and round-trip checks | Python 3; portable and self-contained. |
| Private Python tools | Art conversion, ROM installation, packaging, static checks | Python 3 source is portable in principle; many builders are hash- and release-specific. |
| `tools/emulate.py` | Headless deterministic visual/state harness | Requires NumPy and Pillow plus the bundled Snes9x libretro core. |
| `tools/play.py` | Interactive local player | Also requires pygame-ce and a supported desktop/audio stack. |
| `tools/snes9x/` | Custom Snes9x/libretro source and built core | Source is a Git worktree at `890b5d445538fe790aa3add3d5702c80f551e0ae`, with a 19-line local inspection patch to `libretro/libretro.cpp`. Preserve that revision, its binary diff, source-license material, build recipe, and the current `.so` hash in the private manifest. The binary is Linux/architecture-specific; macOS and Windows builds remain untested and must be re-qualified. |
| Video and capture tools | Native captures, editing, inspection | Python plus external FFmpeg/FFprobe; video subprojects have independent Node package files and lockfile coverage is incomplete. |
| Audio conversion/auditions | Source media to WAV/BRR and previews | Uses local tools and retained artifacts; FFmpeg is observed in scripts. Audio-model environments are optional historical tooling, not required for the v29 ROM rebuild. |
| ASR/model environments | Transcription and source research | Third-party downloads/cache, OS- and Python-specific. Reinstall only when a historical transcription task needs them. |

Private `requirements.txt` pins NumPy 2.5.2, Pillow 12.3.0, and pygame-ce
2.5.8. It does not lock system libraries, FFmpeg, Node, browser tooling, or the
Snes9x build. A clean-machine build therefore requires verification against the
known ROM hash before it can be treated as equivalent.

## Private archive and workbench contents

The archival route is intentionally complete: preserve all authored material,
historical diagnostics, source media, ROMs, saves/states, evidence, and masters
in the private transfer. The observed private work tree was about 25 GiB before
archive exclusions. Large historical areas include `work/turtles` (~3.4 GiB),
`work/cleanup-v12` (~3.2 GiB), `work/cleanup-v11` (~1.8 GiB),
`work/vega` (~1.2 GiB), `work/all-voices-v29` (~1.2 GiB), and
`work/voices-recap-v29` (~1.1 GiB). `data/` was ~157 MiB and `tools/` ~26 MiB.
Sizes are observations, not transfer guarantees.

Include in the private Dropbox archive:

* root authored docs, release guides, `KNOWN-ISSUES.md`, `README*`, and
  `requirements.txt`;
* `tools/` in full, including the `tools/snes9x/` Git source at
  `890b5d445538fe790aa3add3d5702c80f551e0ae`, the local
  `libretro/libretro.cpp` inspection patch, source-license material, build
  recipe, and current libretro core; preserve the core binary as a provenance
  artifact, not a cross-platform runtime promise;
* `data/`, `work/`, `videos/`, and `video-explainer/`, including historical
  diagnostic evidence, masters, raw source media, derived ROMs, native
  captures, save states, and allocation/verification receipts;
* the external pristine headerless 2,621,440-byte input ROM and its verified
  512-byte-headered form in a private legal-media area, with the public
  documented SHA-256 values and a manifest entry. Do not add either to GitHub
  or the public archive;
* the private v28 base ROM and all derived release ROMs already under `work/`.
  They are load-bearing for the verified v29 chain and for historic evidence.

Exclude only reproducible or disposable material: `.git/`, Python virtual
environments such as `.venv` and `asr-env`, `node_modules/`, `__pycache__/`,
browser downloads/profile caches, downloaded ML/ASR model caches, and temporary
extracted video-frame directories. Preserve authored scripts, manifests, logs,
and selected frames that are referenced as evidence. Do not use a broad
`*frame*` deletion rule: several referenced PNGs are evidence and source assets.

The private workbench Git repository should track authored text, source code,
manifests, prompts, ledgers, and small receipts only. Keep binary art, media,
ROMs, states, and capture evidence in the ordinary private Dropbox archive,
not Git LFS. Record an archive manifest with relative paths, byte counts,
SHA-256 values, origin classification, and restore priority.

## Load-bearing external material and path repair

The following material is outside normal authored Python source and must be
accounted for in the private manifest:

| Item | Why it matters | Handoff action |
| --- | --- | --- |
| Pristine legal game ROM | Required by public patch application; original lineage source | Retain privately: the headerless original is 2,621,440 bytes, and the patcher also recognizes its verified 512-byte-headered form. Identify it only by relative path, size, and SHA-256. |
| Derived v28 ROM | Direct, hash-pinned input to v29 | Preserve under private `work/`; verify its SHA-256 before running v29 builders. |
| Snes9x libretro `.so` and its source | Existing verification harness loads it by default | Preserve source revision `890b5d445538fe790aa3add3d5702c80f551e0ae`, local inspection diff, build recipe, license material, and the binary SHA-256. Build a platform-matching core on another OS, then re-run validation. |
| Third-party voice/video media | Source provenance and editable audio/video work | Retain privately with origin/license notes; never publish unless rights permit. |
| FFmpeg/FFprobe | Capture and media verification | Install per host; no bundled executable is required for ROM construction. |
| Python packages | Emulator and image tooling | Create a fresh venv from `requirements.txt`; verify versions and results. |

Some historical manifests and video edit JSON files embed former absolute paths.
They are evidence, not portable commands. Restore the archive under any private
root, replace only path fields needed for an active edit, and preserve the
original receipt alongside the corrected working copy. One known active helper,
`work/all-voices-v29/public-prep/verify_r5_routes.py`, points at a former
Downloads location for a pristine ROM; do not rely on it until it is changed to
an explicit relative input argument or private manifest lookup. No load-bearing
`/tmp` dependency was found in the v29 three-step ROM builder.

## Bounded archive-restore smoke test

Do not run a historical original-ROM rebuild as the first portability check.
Instead, restore a small clean private workbench and reproduce v29 from the
hash-pinned v28 input. This exercises the verified current chain without
claiming more than it proves. This exact bounded smoke test passed on
2026-09-12; its private receipt is `work/handoff-v29-2026-09-12/v29-source-smoke.json`.

The minimum source set for this smoke test is:

* `requirements.txt` and the complete `tools/` directory (the entry scripts
  import older helper modules for DMA/consumer inspection and 65816 assembly);
* `work/fire-fixes-v28/build-final/tmnt-roster-v28.sfc`;
* `work/all-voices-v29/audio/` in full. The active BRR inputs are
  `slash-call.brr`, `rocksteady-call.brr`, `krang-call.brr`, `bebop-a.brr`,
  `bebop-b.brr`, `leatherhead-call.brr`, `april-what.brr`, `april-burst.brr`,
  `april-full-laugh.brr`, `turtle-leo-radical.brr`,
  `turtle-mikey-gnarly.brr`, `turtle-group-cowabunga.brr`, and `silence.brr`;
* an initially empty `work/all-voices-v29/` output area, or the same relative
  target directories after confirming existing candidates carry the expected
  bytes.

Create a fresh venv from `requirements.txt`; NumPy and Pillow are required even
for the first builder because its graphics-consumer audit imports image-aware
historic helper modules. The core `.so`, FFmpeg, Node, source video, and native
capture evidence are not inputs to these three ROM-construction commands.

Restore those paths into a fresh scratch workbench root, so the hard-coded
first-step target cannot overwrite retained evidence. The parsers accept output
file paths, not directories; use this exact sequence from that scratch root:

```sh
python tools/add_actor_voices_v29.py
python tools/finish_private_voices_v29.py \
  --source work/all-voices-v29/actor-routing-r2/tmnt-roster-v29-actor-voice-candidate.sfc \
  --out work/all-voices-v29/combined-r2/voice-candidate.sfc
python tools/finish_voice_events_v29.py \
  --source work/all-voices-v29/combined-r2/voice-candidate.sfc \
  --out work/all-voices-v29/combined-r5/voice-candidate.sfc
sha256sum work/all-voices-v29/combined-r5/voice-candidate.sfc
```

The observed scratch output was byte-identical to canonical v29:
`03e1060d04be410d93d7a87e6668b51e6189d99ba887c526404f2c113df9001a`.
The copied Linux core also cold-booted that scratch ROM for 120 frames and
produced a 256×224 native frame plus state, VRAM, CGRAM, OAM, RAM, and register
captures. The separately retained
`build-final/tmnt-roster-v29.sfc` is the canonical release copy; the final
builder does not create it automatically. This does not establish a rebuild
from a pristine original ROM, native campaign coverage, hardware behavior, or
macOS/Windows core equivalence.

## First boot on another device

1. Restore the private archive to a writable private workbench root. Keep its
   relative directory layout intact.
2. Create a fresh Python virtual environment and install the pinned private
   requirements. Install FFmpeg separately only for media/capture work.
3. Confirm the pristine input ROM and the derived v28 base against their
   recorded SHA-256 values. The public patcher recognizes the verified
   headerless original and its verified 512-byte-headered form; the private v29
   builder requires the recorded derived v28 input.
4. On Linux, first try the archived libretro core with `tools/emulate.py`.
   On another platform, build or obtain a compatible libretro core and consider
   all native-capture comparisons newly unverified until repeated.
5. Run the three v29 builders above in a clean private work tree. Compare the
   final SHA-256 with the known v29 value.
6. Run the relevant static and native verification tools before editing or
   publishing a successor. Preserve the old candidate directories; they are
   evidence of rejected and accepted routing decisions.
7. Clone the public patch repository separately for release packaging and run
   its tests. Copy only public-safe patch artifacts, documentation, and tests
   into that repository after its private-marker audit passes.

## Retired versus current tools

Current release work is v29 and should start with the three v29 builders above,
the v29 guides, allocation reports, and verification receipts. Earlier builders
are retained as historical reproduction, diagnostics, or inputs to newer
releases; their hard-coded hashes and offsets make them unsafe as a generic
"build everything" command. In particular, older character/stage importers
must be adapted with fresh allocation and ownership checks before a new swap.

The public patcher is current for end users. The private emulator harness is
current for the tested Linux environment. Music Lab is paused, and ASR/model
directories are retired/optional research tooling. Native gameplay certification
is evidence from the archived environment, not a claim of exhaustive hardware
or cross-platform emulator certification.
