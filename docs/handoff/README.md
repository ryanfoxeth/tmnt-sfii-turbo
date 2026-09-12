# AI handoff — TMNT × Street Fighter II Turbo

Audited September 12, 2026. Start here before continuing the project or adapting its method to another roster. This is the current navigation layer; versioned release notes preserve historical facts and may describe work that has since been completed.

## The result and the boundary

This is a native **SNES Street Fighter II Turbo, Europe/PAL v1.0 ROM modification**, expanded to 4 MiB. Twelve fighter slots retain their original moves, hitboxes, AI, damage and timing while using TMNT art and presentation. Don and Mikey are alternate costumes of Leo and Raph, giving fourteen identities, not fourteen independent fighter slots. There is no replacement game engine. RayofJay's Windows editor was neither used nor ported: independent Python codecs, importers, assembly patches and a Snes9x/libretro inspection harness were developed on Linux.

Verified playable baseline: **v29**, released September 10, 2026. This documentation update does not create a new ROM version.

| Item | Exact identity |
| --- | --- |
| Original headerless ROM | 2,621,440 bytes; SHA-256 `b8ee1b5b9deae5c84fa209815515030109cc271b645a18de882aaf1b254cda1f` |
| Verified original with 512-byte copier header | SHA-256 `98d0b789a8a0c25bf82c777cba7289faa14365133cb7ea9d822005a1fdca3101` |
| Final v29 | 4,194,304 bytes; SHA-256 `03e1060d04be410d93d7a87e6668b51e6189d99ba887c526404f2c113df9001a`; SNES checksum `9AE3` |
| Playable release commit | [`15593e4`](https://github.com/ryanfoxeth/tmnt-sfii-turbo/commit/15593e41f69424b2aa205577d865cb41f1e0bdc6) |
| Private canonical output | `work/all-voices-v29/build-final/tmnt-roster-v29.sfc` |

## Read in this order

1. [Current state and remaining work](STATUS.md): what is delivered, retained, paused, or still imperfect.
2. [Tools and portability](TOOLS-AND-PORTABILITY.md): restore on another device; patch reproduction versus editable-source reproduction.
3. [Graphics, stages and UI](GRAPHICS-STAGES-UI.md): formats, authoring, shared ownership, allocation and visual traps.
4. [Audio and endings](AUDIO-AND-ENDINGS.md): native music/BRR/events, text, the ending player and motion.
5. [Verification and video](VERIFICATION-AND-VIDEO.md): native evidence, gameplay coverage, CPU demonstrations and correct sound/video capture.
6. [New-reskin playbook](NEW-RESKIN-PLAYBOOK.md): another roster in SFII versus a different ROM entirely.
7. [Ready-to-paste continuation prompts](CONTINUE.md): bring the next AI up to speed without this conversation.

For a focused task, read the index/status and only the relevant technical guide. Do not load every historical report into model context. The private workbench also has an automatically generated tool catalog and per-file transfer manifests.

## Where the project lives

| Location | Contents and purpose |
| --- | --- |
| [This public patch repository](https://github.com/ryanfoxeth/tmnt-sfii-turbo) | Hash-checked BPS patches, portable patcher, selected public art, this handoff and synthetic CI tests. Anyone with the matching original can recreate the playable v29 image. |
| [Private development workbench](https://github.com/ryanfoxeth/sf2-reskin-workbench) | Authored tools, historical technical guides, build/capture scripts and current handoff. Requires Ryan's access. Not a generic finished GUI or standalone art-independent builder. |
| Private Dropbox transfer folder `Automation/TMNT-SFII-Complete-Handoff-2026-09-12` | Full working material, including art masters/prompts, accepted and rejected sources, native evidence, source clips, historical builds/states, customized emulator source and media projects; SHA manifests and restoration instructions. This material stays private. |
| StarDeck: `Ideas/Street Fighter II Turbo — AI Handoff.md` | Device-independent launch note with Git links, private archive location, restore directions, scope and continuation prompt. |
| StarDeck: `Ideas/Street Fighter II Turbo — Custom Characters Plan.md` | Detailed creative decisions, user acceptance, release history and delivery evidence. |

A Git clone of this public repo is enough to **play** v29 with the correct original. Editing the project also needs the private workbench and source materials. A Git clone alone must not be described as the complete authoring workspace. The public patcher is portable; the Linux native authoring/capture environment has not been certified on macOS or Windows.

## Reproduce the released game

From the public checkout, using Python 3.9+:

```bash
python3 apply_patch.py "/path/to/original.smc" --out "/path/to/new/TMNT-SFII-v29.sfc"
python3 -m unittest discover -s tests -v
python3 scripts/audit_public_tree.py
```

Use an absent output filename. The patcher verifies revision and final hash and refuses unsafe or already-current inputs. CI uses synthetic data and needs no ROM; real-ROM reproduction is a separate local check. See [verification](../verification.md) for measured release coverage. Do not strip an arbitrary file header or bypass a hash guard to make a wrong revision pass.

## Working contract for the next AI

- Confirm the user's next requested scope: continuing TMNT, another roster in this SFII ROM, or a different game. Mortal Kombat was an example, not an approved character-to-slot mapping or a request to start production now.
- Start from the exact accepted version and preserve it. Old builders often rebuild from older inputs; they are not cumulative install commands.
- Track every ROM/WRAM/VRAM/APU reservation and every shared consumer. A zero-filled bank tail is not evidence of free space.
- Preserve original combat behavior unless explicitly asked to change it. Art must fit registered native poses; SNES does not impose one universal fighter height.
- Use small visual pilots and bounded, fresh-context workers. One integrator owns the final ROM and allocation ledger; run expensive emulator/image/media work serially at low priority.
- Copy verified versioned ROMs to the shared `ROMS` folder, preserve prior files, compare hashes and confirm cloud sync. Keep experiments under private `work/`.
- Public source changes need scoped staging, tests and the file audit. Never copy the private workspace into the public repo. Existing distribution rules remain in [CONTRIBUTING](../../CONTRIBUTING.md).
- Update StarDeck's project note and the actual local date's daily log after repository work. Document exact output/hash, changed resources, commands, validation limits, approvals and next step.

## What “complete handoff” means here

The method, code, source materials, decisions, failed approaches, release identity and verification records are preserved and indexed. This is **not** a claim that the game has no remaining art imperfections, that all historical commands run unchanged on another OS, or that arbitrary character art can be imported in one command. The portable baseline and the full private source transfer are separate layers so a new AI can resume without reconstructing this chat.
