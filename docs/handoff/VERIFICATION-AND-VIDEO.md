# Verification, native capture, and media handoff

Use this with [Audio and ending-engine handoff](AUDIO-AND-ENDINGS.md) and the
public [verification record](../verification.md). It documents measured scope,
not a claim of complete emulator or console coverage. Private rebuild and
capture utilities require the private workspace, its hash-pinned inputs, and
the recorded dependency setup; they are not shipped in this repository.

The complete authoring workbench is intentionally private and archived
separately. It retains source art/media, native proof, historical capture
states, generated intermediates, and delivery receipts needed to repeat a
reskin. This public repository is the portable patch distribution and a
technical map to that workbench; it is not an all-inclusive authoring archive.
Historical receipts can contain machine-specific delivery paths. Treat them as
evidence records and rebase them to the restored workbench root rather than
following those paths verbatim.

## Build and QA order

For a release candidate, first reproduce the owned component build from its
exact prior release, inspect allocation ledgers, and confirm the output hash.
Then run static ownership/preservation checks before native playback. Capture
only after native route evidence passes. A public package is validated
separately with the repository patcher, BPS round trips, unit tests, and
`python3 scripts/audit_public_tree.py`; it contains patches and allowlisted
documentation, never a complete ROM, private state, or standalone source media.

Native jobs are resource constrained. Run one emulator/encoder workload at a
time, low priority, with one numeric thread and two CPU cores:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n10 taskset -c0,1 <command>
```

Do not run parallel capture/render jobs, reuse stale states as proof, or infer
an accepted release from a candidate filename. A health fixture may accelerate
fights, but QA must still use controller progression through the real game; it
must not force a winner, ending identity, scene, phase, or title return.

## Ending-specific native QA

`tools/verify_tmnt_endings_v23.py --rom <candidate> --out <receipt>` is the
campaign runner; use its identity route rather than a hand-edited state. The
v24 component check is `tools/verify_ending_motion_v24.py --component-only`.
It establishes owned differences, resource preservation, and motion-data
contracts; the full historical verifier/campaign evidence remains required for
release scope. `tools/verify_finish_v25.py <identity> <mode>` checks same-ROM
v25 ending audio and first-page equivalence, and
`tools/capture_finish_v25.py` records the checked Leo review clip.

For v24, `tools/capture_ending_motion_v24.py --identity <identity>` uses
same-ROM campaign states, empty controller ports, native PAL timing, and
same-run stereo audio. Capture 400-frame story and 200-frame credit pages
without overlays. Retain lossless RGB masters; phone exports are H.264/yuv420p
with AAC. The video check compares lossless frame references, not just a
center-screen still. Native ending audio fades near the beginning of these
cards and is then silent; that is expected.

V23's verified campaign matrix reached all stages, bonuses, pages, title, and
menu for 14 Turbo and two Normal-alternate routes. It recorded 382 real KO
transitions, though April Turbo and Mikey Normal each recorded 23, so do not
state that every route demonstrated 24. V24 added 98 GPU pages and two full
loops per story/credit page, with exact effect payloads, CGRAM, and all pixels
outside the intended motion region. V25's two final same-ROM campaigns reached
the same navigation path with 47 fixture KOs total. These scopes are strong
integration evidence, not physical-hardware certification.

## Audio and combat QA

For voice changes, check both sound-bank placements, actual event timing,
sample hashes, instrument/tuning/envelope data, ENDX completion where relevant,
and preservation of non-vocal/global DSP behavior. V28's focused fire evidence
uses four fresh controller routes: both positions for Slash/Leatherhead burns
and all seven Splinter flame poses in both directions (1,448 frames). A prior
helper sampled fighter RAM at setup time; that old RAM claim is invalid.
Current helpers must refresh live RAM every frame. Cached visual pointers may
be masked only when documented and their resolved visual payload remains exact.

V29 adds 24 voice component routes, second-side coverage, both alternate
turtles, focused attacks/wins/KOs, and two Normal routes. Its fresh Slash Turbo
campaign covers 39,163 frames, 24 KOs, all 12 stages, all three bonuses, seven
ending/credit pages, and title/menu return. The scope does not establish every
move, every audio mix race, exhaustive cross-ROM frame identity, listening
acceptance, or hardware behavior.

For music experiments, preserve the paused status. The one existing native
Music Lab run proves a bounded preview, title/stage upload checks, and a combat
smoke test; fast cue `0x21` did not trigger in its VS fixture. It is not release
QA and does not prove complete music transitions, pause/resume, or mix quality.

## Video workflow and AAC seam correction

The v29 voice showcase and daily recap are editorial exports from native,
same-run game captures. Their source ledgers are private-workspace-relative:
`videos/voices-recap-v29/README.md`, `work/voices-recap-v29/native/`,
`work/voices-recap-v29/native-extra/`, and the project `edit.json` files.
The native picture and PCM arrive from the same emulator callbacks; source audio
clock quantization is below 0.11 ms. The final render is 1280×720, 50 fps,
preserving the original 4:3 game geometry without crop. It adds minimal labels,
no narration, synthetic speech, or external music.

Run the video steps in this order:

1. Build the prefix and voice projects with `tools/build_voice_recap_v29.py`
   using `prefix` and `voices` modes.
2. Verify each rendered project with
   `tools/verify_voice_recap_v29_media.py <project> <video> <out>`; require a
   full decode, source-aligned audio, and its verification receipt.
3. Stage the two final films with `tools/package_voice_recap_v29_videos.py`.
   This tool performs the final decode and exact picture-frame concatenation
   checks before copying staged media.

Do **not** directly concatenate AAC streams. AAC priming/padding caused a
timestamp mismatch at the original prefix/showcase boundary. The approved
method stream-copies every video packet, decodes each native mix to the exact
48 kHz sample count implied by its source duration, joins those PCM samples,
and encodes the continuous audio once as AAC. Both output streams begin at zero.
The final delivery retained every video packet, was not rendered twice, passed
full decodes and 43 section-frame inspections, and had per-section audio
correlation at least 0.99731 across 8,968 picture-frame comparisons.

The videos demonstrate controlled, logged health fixtures and selected voice
events. They are not competitive CPU-match evidence. Shared turtle calls repeat
by design; the short Shredder laugh was not separately captured. The ending-art
montage uses a stock native ending-cue recording as an editorial bed, without
dubbing a character line onto unrelated gameplay. The Music Lab footage is
explicitly labeled experimental/paused and is not part of the released ROM.

## Checklist for a future reskin

- Pin the base release hash and preserve every existing allocation ledger.
- Rebuild each component in its documented order; reject overlap and verify
  every unrelated resource claimed preserved.
- Exercise actual controller routes in both sides/modes and both audio banks.
- Use fresh-boot or same-ROM campaign states for any release claim.
- Record the exact test scope, fixture use, checksums, and remaining gaps.
- Keep public packages to patches, portable tools, allowlisted docs, and
  evidence summaries. Do not publish complete ROMs, emulator states, or source
  media.
