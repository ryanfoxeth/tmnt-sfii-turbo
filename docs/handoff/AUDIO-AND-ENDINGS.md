# Audio and ending-engine handoff

This is an implementation handoff for the private reskin workspace. The public
repository contains the v29 patch distribution and tests, but not the private
ROM build inputs, emulator states, source recordings, BRR assets, or native
tooling. Start with the private workspace's `AGENTS.md`, current allocation
ledgers, and hash-pinned release receipts before changing any resource.

The released v29 target is documented in [the release record](../releases.md#v29--fighter-voices).
It retains original stage music, hits, and non-vocal effects; stock short shared
hurt grunts and April's KO scream are intentional. The turtle idle remains open.
Music Lab is intentionally paused: preserve the stock soundtrack and do not
resume arrangements without a new product decision.

## Audio: build order and contracts

The v29 build is deliberately staged. Run these private-workspace entrypoints
in order against their hash-pinned inputs:

1. `tools/add_actor_voices_v29.py` produces `work/all-voices-v29/actor-routing-r2/`.
2. `tools/finish_private_voices_v29.py --source <actor-routing-r2> --out <combined-r2>`
   installs the selected private samples and complete-phrase cues.
3. `tools/finish_voice_events_v29.py --source <combined-r2> --out <final>`
   adds the isolated commands and event hooks.

Do not skip stages, apply the latter tools to a different base, or treat a
similarly named candidate as a release. The final tool's expected source is the
combined result. Its report and the final verification records under
`work/all-voices-v29/` are the authoritative evidence.

The sound loader has two active sequence banks. Resource `0x32` is the combat
bank; resource `0x01` replaces it for victory/menu sequences. Any sound change
that works only in one bank is incomplete. A sequence payload begins with the
command count and master volume; command pointers begin at **payload + 2**.
The instrument table base is **APU `0x29C4`**. Do not use the rejected `+4`
pointer interpretation or an `0x2994` instrument base.

V29 grows each bank from `0x4C` to `0x50` commands. Existing `0x19`/`0x1A`
combat entries were already referenced, so they are restored rather than
repurposed. New actor-only commands are `0x4C..0x4F` in both banks:

| Command | Program slot | Purpose |
| --- | --- | --- |
| `0x4C` | `0x25` | extra actor slot, placement A |
| `0x4D` | `0x2D` | extra actor slot, placement B |
| `0x4E` | `0x1E` | first private slot, placement A |
| `0x4F` | `0x26` | first private slot, placement B |

Relocate every command, track, and branch pointer when the table expands. The
private builder performs a reversible semantic round trip; preserve that check.
Sample edits must retain valid non-looping BRR endings and fit their native
allocation. The shared turtle resource has a 9,000-byte native sample limit.

Actor isolation is resource routing, not a palette/name change. V29 gives
Rocksteady copies in resources `0x03/0x04`, Slash new banks `0x05/0x06`, and
extends Krang's `0x50/0x51` transfers while retaining its original records.
Keep common sources intact and retain all earlier allocation ownership. V29
uses runtime ranges `0x32CE00..0x32CE30` and `0x32CE40..0x32CED6`, combat data
`0x32F000..0x32FEBB`, and victory data `0x337000..0x337A67`; these coexist with
the paused Music Lab reservation `0x323C00..0x324111`, F2 text, portraits, and
prior live reservations. Empty bytes alone are not safe allocation.

Two hooks are intentionally narrow. The `0x0B53` hook changes event `0x20`
only for Slash on real fighter direct pages `0x0500/0x0700`; preserve the full
accumulator and do not generalize a transient selector. The `0x0B1E` hook adds
one voice alongside the native round-win jingle only for Leatherhead, Slash,
Krang, and Rocksteady, and only when there is a fighter stage, audio enabled, a
populated winner buffer, one defeated opponent, and a living winner. Preserve
the displaced prologues, register/status stacks, and jingle. The four replaced
victory vocal cues are intentionally muted; unrelated score and Slash bone
effects remain.

## Ending engine: native constraints

The ending player is shared. Its real dispatcher hook is `C0:32F8`; `C0:7868`
is an immediate operand and must never be hooked. `WRAM 0x1965` is the stock
ending selector. For Leo/Don and Raph/Mikey, derive the alternate identity from
saved winner costume `0x18B5` minus mode `0x1C84` (`0x20` identifies Don/Mikey).
Do not globally normalize costume state.

Packet order is Leo, Don, Bebop, Leatherhead, Casey, Raph, Mikey, April, Slash,
Splinter, Krang, Super Shredder, Rocksteady, Shredder. `C6=FE` denotes the
ending engine; `C7=1..2` are story pages, `3..7` are credits, and `C7=0` means
completion. `C6` remains `FE` at the title, so title QA must use `C7`, never
infer an active ending from `C6` alone.

The v23 packets own two art ranges and code/data space recorded in
`work/endings-v23/allocation-ledger.json`. BG1 uses VRAM `0x2000..0x3800`, map
`0x8000`, and CGRAM palette groups 2–4. BG3 ending text uses private glyphs
`0x4000..0x4800` and map `0x7000`. Preserve native font `0xA000`: replacing it
corrupts ranking/menu text. The normal scanline IRQ releases frame gate
`0x1842`; NMI-only mode freezes the scheduler. Use the ordinary IRQ and normal
NMI path (`0x1843=0`), and do not confuse `0x184B` with the normal TM shadow
(`DP BF`). Disable inherited windows, HDMA, and queued map DMA before drawing a
new still.

For v24 motion, compile art first with `tools/ending_motion_art_v24.py`, then
build the engine with:

```text
tools/ending_motion_engine_v24.py --base <exact-v23> --motion-data work/ending-motion-v24/art/motion-data.bin --out <v24-output>
```

Phase zero must equal v23 exactly. Use only localized changes inside the
approved 128x96 art bounds; the on-screen art origin is `(64, 23)`. The runtime
is `0x31D382..0x31D492`, motion data is `0x320800..0x323B40`, and the native
font at `0x31D800` stays untouched. The tick hook at `0x31D019` is a tail JML;
the page hook at `0x31D263` is a JSL reset. The tail exit must return to
`F1:D034` so `SEP #$20` runs before `INC C7`; `D036` skips it.

Motion writes only the game's normal-NMI DMA queue at `0x0300`. `A4` is queue
**byte length**, not descriptor count. Each eight-byte descriptor uploads one
32-byte 4bpp tile using `VMAIN=0x80`, bounded to 16 descriptors / 512 bytes per
scheduled update. Do not overwrite a nonempty queue (`A4 != 0`), push a return
address per tick, use global palette cycling, replace full scene art, change
the NMI handler, or change gameplay IRQ/visible PPU state. Keep `D2` as the
costume-aware packet selector; `D9..DD` are independent ending scratch.

The v25 ending soundtrack is stock native cue `0x28`, which plays through the
ending and fades using native `F6/Y08` before ranking cue `0x2F` and title cue
`0x11`. `BC93 + cue` is an optional instrument-bank selector, not a sequence
redirect table. This does not constitute replacement music.

## Paused Music Lab

`tools/music_lab_server.py --port 8768` serves the private loopback arranger;
`tools/music_lab_native.py --rom <base> --out <job> --seconds <n>` makes one
native preview. It is an experiment, not a release build. Its sequence window
is 3,200 bytes at APU `0x0D20..0x199F`, with a conductor and at most six audible
tracks. Program IDs `0x00..0x1B` are native IDs, not verified instrument names.
No new samples or voices are allocated.

Keep native previews serial, low priority, single-threaded numeric work, and
within the experiment's storage limit. The importer quantizes to three native
ticks, rejects unsupported controls such as sustain/pitch bend, uses fixed
mapping/volume overrides, and does not reproduce per-note velocity. Track
ends/loops must agree at a positive tick; ties, slurs, persistent program, and
octave state are importer invariants. The existing demo verified title/stage
uploads and a combat smoke test, but its VS fixture did not trigger fast cue
`0x21`; do not claim that transition, broad mix coverage, subjective approval,
or hardware certification.

## Evidence and remaining scope

The private v29 evidence includes 24 voice component routes, focused both-side,
KO, and Normal checks, plus a fresh Slash Turbo Arcade campaign of 39,163
frames, 24 KOs, all 12 stages, three bonuses, seven ending/credit pages, and a
title/menu return. It also checks preservation of the original songs, common
resources, accepted private voices, 1,962 graphics consumers, and 27 scene
graphs. Sample-upload timing can shift initial emulator phase; this is neither
exhaustive frame identity nor physical-hardware certification. Audio captures
are technical evidence, not subjective listening approval.

Ending QA historically covers 14 Turbo identities plus Normal Don/Mikey,
98 ending pages, and complete motion loops. Health fixtures accelerate matches;
they do not force ending identity, scene, phase, or script. V25 adds two
same-ROM campaigns (Turbo Leo and Normal Mikey), 47 observed fixture KOs, and
native ending-audio/page checks. It does not prove every possible match, pose,
or hardware behavior. Use fresh boots and same-ROM states; never present a
diagnostic cross-ROM state as release proof.
