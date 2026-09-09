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

V17_SHA256 = 'f0cf0064765bef202e75d5c7a664ff9406cfdba6e55bbaad16813d7d8ccd9daa'
V17_PATCH = "tmnt-sfii-turbo-v16-to-v17.bps"
PATCH_SHA256.update({'tmnt-sfii-turbo-v17.bps': '41272fcffd6785b504df73494ab6b3c903f320f94a6b5e5cc9598dd89562266c', 'tmnt-sfii-turbo-v16-to-v17.bps': '5e26d62d89066ae89f606671582b16b661e90edbe6bd38ef6620f08457ef0a04'})

V18_SHA256 = '0e1e06361f4b21cddf425adb8b9fb072157cb32db1609aef609bcec7cadd7c20'
V18_PATCH = 'tmnt-sfii-turbo-v17-to-v18.bps'
PATCH_SHA256.update({'tmnt-sfii-turbo-v18.bps': '4a4be276c845b43b9e9a36ee09ffbbc198233f8f8b89d81acf85de76c546e86f', 'tmnt-sfii-turbo-v17-to-v18.bps': '3a4b815ec4ec1aa54e805a3bf11a145825ad92b46d4296c48576272ea381f5a6'})

V19_SHA256 = 'a1cbd12ab115b81cfd7e970f4e331329715d0168ed0edb2c62a67c8ae5f7aec1'
V19_PATCH = 'tmnt-sfii-turbo-v18-to-v19.bps'
PATCH_SHA256.update({'tmnt-sfii-turbo-v19.bps': '055c3ae7aa0fcb99b59a6661e875774702229e17a52a538a168874e8addd2db9', 'tmnt-sfii-turbo-v18-to-v19.bps': '46902d9035ec1d65e3335ae56329938bc18bac16650344d7b6af061a47f9f34b'})


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def choose_patch(input_bytes: bytes):
    digest = sha256(input_bytes)
    if digest == V19_SHA256:
        raise BPSError("input is already the v19 release; no patch is needed")
    if digest == V18_SHA256:
        return input_bytes, PATCHES / V19_PATCH
    if digest == V17_SHA256:
        return input_bytes, PATCHES / V18_PATCH
    if digest == V16_SHA256:
        return input_bytes, PATCHES / V17_PATCH
    if digest in V16_PATCHES:
        return input_bytes, PATCHES / V16_PATCHES[digest]
    if digest == HEADERED_BASE_SHA256:
        if len(input_bytes) < 512 or sha256(input_bytes[512:]) != BASE_SHA256:
            raise BPSError("recognized headered ROM did not yield the expected base ROM")
        return input_bytes[512:], PATCHES / V16_PATCHES[BASE_SHA256]
    raise BPSError("input SHA-256 is not a supported original, v12, v13, v14, v15, v16, v17, or v18 revision")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="supported original, v12, v13, v14, v15, v16, v17, or v18 ROM")
    parser.add_argument("--out", required=True, type=Path, help="new v19 output file")
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
        if patch_path.name not in (V18_PATCH, V19_PATCH):
            if patch_path.name != V17_PATCH:
                if sha256(target) != V16_SHA256:
                    raise BPSError("intermediate ROM SHA-256 does not match v16")
                upgrade = (PATCHES / V17_PATCH).read_bytes()
                if sha256(upgrade) != PATCH_SHA256[V17_PATCH]:
                    raise BPSError("v17 upgrade patch SHA-256 does not match")
                target, _ = apply_bps(target, upgrade)
            if sha256(target) != V17_SHA256:
                raise BPSError("intermediate ROM SHA-256 does not match v17")
            upgrade = (PATCHES / V18_PATCH).read_bytes()
            if sha256(upgrade) != PATCH_SHA256[V18_PATCH]:
                raise BPSError("v18 upgrade patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name != V19_PATCH:
            if sha256(target) != V18_SHA256:
                raise BPSError("intermediate ROM SHA-256 does not match v18")
            upgrade = (PATCHES / V19_PATCH).read_bytes()
            if sha256(upgrade) != PATCH_SHA256[V19_PATCH]:
                raise BPSError("v19 upgrade patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if sha256(target) != V19_SHA256:
            raise BPSError("patched ROM SHA-256 does not match the v19 release")
        # Exclusive creation keeps the no-overwrite guarantee even if another
        # process creates the destination after the check above.
        with args.out.open("xb") as output:
            output.write(target)
    except (OSError, BPSError) as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    print("Wrote {} (SHA-256: {})".format(args.out, V19_SHA256))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
