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
PATCH_SHA256 = {
    "tmnt-sfii-turbo-v13.bps": "c2a07f402fb51e05b2c7dfadc3ea8075edaaeb57a98a56ebbb4033f476ba52fc",
    "tmnt-sfii-turbo-v12-to-v13.bps": "13329af6049b750b3a969c36133eb56eec7730d4ef40295b2e4b6c13c826f1e7",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def choose_patch(input_bytes: bytes):
    digest = sha256(input_bytes)
    if digest == BASE_SHA256:
        return input_bytes, PATCHES / "tmnt-sfii-turbo-v13.bps"
    if digest == HEADERED_BASE_SHA256:
        if len(input_bytes) < 512 or sha256(input_bytes[512:]) != BASE_SHA256:
            raise BPSError("recognized headered ROM did not yield the expected base ROM")
        return input_bytes[512:], PATCHES / "tmnt-sfii-turbo-v13.bps"
    if digest == V12_SHA256:
        return input_bytes, PATCHES / "tmnt-sfii-turbo-v12-to-v13.bps"
    raise BPSError("input SHA-256 is not the supported original or v12 revision")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="supported original or v12 ROM")
    parser.add_argument("--out", required=True, type=Path, help="new v13 output file")
    args = parser.parse_args(argv)
    if args.out.exists():
        parser.error("refusing to overwrite existing output: {}".format(args.out))
    try:
        source, patch_path = choose_patch(args.input.read_bytes())
        patch = patch_path.read_bytes()
        if sha256(patch) != PATCH_SHA256[patch_path.name]:
            raise BPSError("patch SHA-256 does not match the published release")
        target, _ = apply_bps(source, patch)
        if sha256(target) != V13_SHA256:
            raise BPSError("patched ROM SHA-256 does not match the v13 release")
        # Exclusive creation keeps the no-overwrite guarantee even if another
        # process creates the destination after the check above.
        with args.out.open("xb") as output:
            output.write(target)
    except (OSError, BPSError) as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    print("Wrote {} (SHA-256: {})".format(args.out, V13_SHA256))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
