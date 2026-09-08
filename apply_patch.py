#!/usr/bin/env python3
"""Apply the appropriate TMNT SFII Turbo release patch offline."""

import argparse
import hashlib
from pathlib import Path
import sys

from bps import BPSError, apply_bps


ROOT = Path(__file__).resolve().parent
PATCHES = ROOT / "patches"
BASE_SHA256 = "b8ee1b5b9deae5c84fa209815515030109cc271b645a18de882aaf1b254cda1f"
HEADERED_BASE_SHA256 = "98d0b789a8a0c25bf82c777cba7289faa14365133cb7ea9d822005a1fdca3101"
V12_SHA256 = "8811ac47e3dd3a7535383fe561108929aa583e715aa7157aa166b50566141796"
V13_SHA256 = "461290feac2c13846a50b30bf8b69a744a8f0f7b8aca9c5421d1413b619455ae"
V14_SHA256 = "aacc2ada6569d35711227d83f179f7ff232a442a1a07b534d0499f0971792d91"
V15_SHA256 = "789a855967a399e10590e500566a5a400d775fe32452a6777201d836afb315f7"
# Published cumulative v16 target and pinned patch hashes.
V16_SHA256 = "389c89355c252d3ad5e8dca5f73e66ad23a27254e094e30ce310b1a37371de71"
PATCH_SHA256 = {
    "tmnt-sfii-turbo-v13.bps": "c2a07f402fb51e05b2c7dfadc3ea8075edaaeb57a98a56ebbb4033f476ba52fc",
    "tmnt-sfii-turbo-v12-to-v13.bps": "13329af6049b750b3a969c36133eb56eec7730d4ef40295b2e4b6c13c826f1e7",
    "tmnt-sfii-turbo-v16.bps": "86b0da6c612e31c17dc7e75e338836bce30b69a31b5634cc2fd6f1d84fb9640a",
    "tmnt-sfii-turbo-v12-to-v16.bps": "209ee33de43780a3a6dd5ae18c5f7d209baff7cbaa1e2262eb57fe5997e1eadb",
    "tmnt-sfii-turbo-v13-to-v16.bps": "d9629bf2d61c8466265791b90970212720c6db40f020cbf438c8110eff25c225",
    "tmnt-sfii-turbo-v14-to-v16.bps": "9d72cfc01b1fc678ce4a462034f56580bafffeea61b56fdb51e57b67db6ce0e0",
    "tmnt-sfii-turbo-v15-to-v16.bps": "55bf6e3e788044b2d5f2cb21388b51ddc0ee3b7c0b4489bb19af898547fb0c8b",
}
V16_PATCHES = {BASE_SHA256: "tmnt-sfii-turbo-v16.bps", V12_SHA256: "tmnt-sfii-turbo-v12-to-v16.bps", V13_SHA256: "tmnt-sfii-turbo-v13-to-v16.bps", V14_SHA256: "tmnt-sfii-turbo-v14-to-v16.bps", V15_SHA256: "tmnt-sfii-turbo-v15-to-v16.bps"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def choose_patch(input_bytes: bytes):
    digest = sha256(input_bytes)
    if digest in V16_PATCHES:
        return input_bytes, PATCHES / V16_PATCHES[digest]
    if digest == HEADERED_BASE_SHA256:
        if len(input_bytes) < 512 or sha256(input_bytes[512:]) != BASE_SHA256:
            raise BPSError("recognized headered ROM did not yield the expected base ROM")
        return input_bytes[512:], PATCHES / V16_PATCHES[BASE_SHA256]
    raise BPSError("input SHA-256 is not a supported original, v12, v13, v14, or v15 revision")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="supported original, v12, v13, v14, or v15 ROM")
    parser.add_argument("--out", required=True, type=Path, help="new v16 output file")
    args = parser.parse_args(argv)
    if args.out.exists():
        parser.error("refusing to overwrite existing output: {}".format(args.out))
    try:
        source, patch_path = choose_patch(args.input.read_bytes())
        patch = patch_path.read_bytes()
        expected_patch = PATCH_SHA256.get(patch_path.name, "")
        if not expected_patch:
            raise BPSError("patch metadata is missing from the published release")
        if sha256(patch) != expected_patch:
            raise BPSError("patch SHA-256 does not match the published release")
        target, _ = apply_bps(source, patch)
        if not V16_SHA256 or sha256(target) != V16_SHA256:
            raise BPSError("patched ROM SHA-256 does not match the v16 release")
        # Exclusive creation keeps the no-overwrite guarantee even if another
        # process creates the destination after the check above.
        with args.out.open("xb") as output:
            output.write(target)
    except (OSError, BPSError) as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    print("Wrote {} (SHA-256: {})".format(args.out, V16_SHA256))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
