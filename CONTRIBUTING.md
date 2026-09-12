# Contributing

Issues and focused pull requests are welcome. For a visual bug, include the
release version, original ROM hash, emulator/version, character, opponent,
stage, player side and the inputs that trigger it. A short relevant screenshot
or recording is more useful than an emulator save state. Do not attach ROMs,
save states, extracted original assets or unrelated personal information.

Keep each change small and independently reviewable. Preserve existing moves,
hitboxes, other fighters, world-map scenes and bonus stages. Test actual game
playback: a clean exported sprite or tilemap does not prove clean animation.

For a patch-tool change, run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/audit_public_tree.py
```

Tests use synthetic bytes, so CI needs no game ROM. Real-game rebuilds should
run locally with files outside the repository. Include hashes and a compact
test summary rather than uploading generated ROMs or emulator state dumps.

For artwork contributions, describe the source and what permission you have
to submit it. The tool-code license does not grant rights to third-party
characters or game assets. Please do not copy sprite sheets from commercial
games into this repository.

For authoring work, start with the [complete AI handoff](docs/handoff/README.md)
and [new-reskin playbook](docs/handoff/NEW-RESKIN-PLAYBOOK.md). The private
workbench and full source transfer are separate from this public distribution.
Avoid promising a complete native source rebuild from this repository alone.
