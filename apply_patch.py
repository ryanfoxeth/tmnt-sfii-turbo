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

V20_SHA256 = '69a71550ed6e9badfd4f2b277b4668b575f7d450ab250cd40604c12ea6dc6fbb'
V20_PATCH = 'tmnt-sfii-turbo-v19-to-v20.bps'
PATCH_SHA256.update({'tmnt-sfii-turbo-v20.bps': '3c8e8488017b868099ad1e3511baedb1a6ec9e57ee65a3189349b83646cab481', 'tmnt-sfii-turbo-v19-to-v20.bps': '771c9269a7a463267118b96ab2001996d651a730adc10156dd710fef5b60f86c'})

V21_SHA256 = '27bab79c6cf21c284f9aa52d396088cdc8f1d8bd7983683d1e51e1a826dc8671'
V21_PATCH = 'tmnt-sfii-turbo-v20-to-v21.bps'
PATCH_SHA256.update({'tmnt-sfii-turbo-v21.bps': 'd13799cb9ba4d491eb9f6c02e22bca2d26421e6e5993f98f92db4a698b3a16cf', 'tmnt-sfii-turbo-v20-to-v21.bps': '37c53fbf8a8b49a44acc2ae70c053ef5a1d912c7e9da209a60e4f35e96856e36'})

# v22 BPS artifacts and hashes are pinned by final release metadata.
V22_SHA256 = 'fe12e8693eb985e1318f1652a9be837090ad4c4ceff4eaa0fef880eb5749ddba'
V22_PATCH = 'tmnt-sfii-turbo-v21-to-v22.bps'
V22_FULL_PATCH = 'tmnt-sfii-turbo-v22.bps'
V22_PATCH_SHA256 = 'bcd2dba4823b5327917c281b5206c5a2669562da981a94f136c36faaae08bb3e'
V22_FULL_PATCH_SHA256 = '54498426698c7d35ceb347642a4c322784e01d4e5a8f3b5c2a9a93a583a5f437'

V23_SHA256 = '44bed3f90b327db71377a3b09542cc287e35a95fcb6eafffedeb81683bb2cdb1'
V23_PATCH = 'tmnt-sfii-turbo-v22-to-v23.bps'
V23_FULL_PATCH = 'tmnt-sfii-turbo-v23.bps'
V23_PATCH_SHA256 = '27519ca0023ccafcda6a3d7a39b62d4f6ede9152f86298d5ff44318ec438519b'
V23_FULL_PATCH_SHA256 = '4df54d5cffe9acbb1370278a34120d7926bd09b180d7e0ce835827e47052e6f5'

# v24 bounded ending-motion BPS artifacts and hashes.
V24_SHA256 = 'c629124fd0020bbca92803ac4e6b8bc630c9e98385e6750fcc5cb644762c19a0'
V24_PATCH = 'tmnt-sfii-turbo-v23-to-v24.bps'
V24_FULL_PATCH = 'tmnt-sfii-turbo-v24.bps'
V24_PATCH_SHA256 = '17f46bf12b21a657584bb7c208b845eeb27c88af8d16ab26f6abc3673e351e6a'
V24_FULL_PATCH_SHA256 = '82692fca5805e9a6fac7962424591c82d98d8b5a51262f0b7c6929b032b71b35'

# v25 final-package staging metadata; populated only for a supplied final ROM.
V25_SHA256 = '59a52734d56110ba15c862d2966856c4e3d8cb69a54e9ccc774e4815c27e6f78'
V25_PATCH = 'tmnt-sfii-turbo-v24-to-v25.bps'
V25_FULL_PATCH = 'tmnt-sfii-turbo-v25.bps'
V25_PATCH_SHA256 = '06e82705d37f373edcba57b7721477875a66db2c647f60e0c07e0d0a09cf99c8'
V25_FULL_PATCH_SHA256 = '289a465f3a431cdd5c9bbbb3491547ad92ab62718be726eff130134698e67471'

# v26 bounded Shredder victory-voice release metadata.
V26_SHA256 = '3b7cdb3d32752fbd348e9e51ee765a472b9b8362d3a6becf003eb51e6cb4c957'
V26_PATCH = 'tmnt-sfii-turbo-v25-to-v26.bps'
V26_FULL_PATCH = 'tmnt-sfii-turbo-v26.bps'
V26_PATCH_SHA256 = '1602a8a253e97be83fdc44489c1c6ea48ec9a35daf7e721c575e1fbf1142d36d'
V26_FULL_PATCH_SHA256 = 'e00a7806fa4fce748780dcdc535f3db03df42600224c0adf633fc10e1d68e87f'


# v27 Super Shredder private pitch adjustment.
V27_SHA256 = '766216af20b5d38acd63cfb334819ca92c5463e7e27a7a7b6e56839311794ed1'
V27_PATCH = 'tmnt-sfii-turbo-v26-to-v27.bps'
V27_FULL_PATCH = 'tmnt-sfii-turbo-v27.bps'
V27_PATCH_SHA256 = '481405fccc22dac9f70d630b50b3c3b5045f802dc64ded9ce85fb1683bc5cd09'
V27_FULL_PATCH_SHA256 = 'e9f566ea5176f8388cf40107262740ed0360b943b2bcca3c0d77acafff0fd96d'

# v28 approved Casey/Splinter voices and Slash/Splinter fire-art repairs.
V28_SHA256 = '72d15ae80928b3ede4a94a3e58ff46a3ae93a9d786151b4e4f5f3ca26a4e2a3b'
V28_PATCH = 'tmnt-sfii-turbo-v27-to-v28.bps'
V28_FULL_PATCH = 'tmnt-sfii-turbo-v28.bps'
V28_PATCH_SHA256 = 'fc7af3e8e51304b146ea88bd516e31c1d35f06a0736fdf80f734904d3bb41095'
V28_FULL_PATCH_SHA256 = '8084b6f6f3582894b5d8eb982c3175eeca3dbbf45ba5e479cbc90f188c453919'

def _require_release_metadata():
    if not V22_PATCH_SHA256:
        raise BPSError('v22 patch metadata is pending final QA and BPS generation')
    if not V23_PATCH_SHA256:
        raise BPSError('v23 incremental patch metadata is missing from the published release')
    if not V24_PATCH_SHA256:
        raise BPSError('v24 incremental patch metadata is missing from the published release')
    if not V25_PATCH_SHA256:
        raise BPSError('v25 incremental patch metadata is missing from the staged package')
    if not V26_PATCH_SHA256:
        raise BPSError('v26 incremental patch metadata is missing from the staged package')
    PATCH_SHA256[V22_PATCH] = V22_PATCH_SHA256
    if V22_FULL_PATCH_SHA256:
        PATCH_SHA256[V22_FULL_PATCH] = V22_FULL_PATCH_SHA256
    PATCH_SHA256[V23_PATCH] = V23_PATCH_SHA256
    if V23_FULL_PATCH_SHA256:
        PATCH_SHA256[V23_FULL_PATCH] = V23_FULL_PATCH_SHA256
    PATCH_SHA256[V24_PATCH] = V24_PATCH_SHA256
    if V24_FULL_PATCH_SHA256:
        PATCH_SHA256[V24_FULL_PATCH] = V24_FULL_PATCH_SHA256
    PATCH_SHA256[V25_PATCH] = V25_PATCH_SHA256
    if V25_FULL_PATCH_SHA256:
        PATCH_SHA256[V25_FULL_PATCH] = V25_FULL_PATCH_SHA256
    if not V27_PATCH_SHA256:
        raise BPSError('v27 incremental patch metadata is missing')
    PATCH_SHA256[V27_PATCH] = V27_PATCH_SHA256
    if not V28_PATCH_SHA256: raise BPSError("v28 incremental patch metadata is missing")
    PATCH_SHA256[V28_PATCH] = V28_PATCH_SHA256
    PATCH_SHA256[V28_FULL_PATCH] = V28_FULL_PATCH_SHA256
    PATCH_SHA256[V27_FULL_PATCH] = V27_FULL_PATCH_SHA256
    PATCH_SHA256[V26_PATCH] = V26_PATCH_SHA256
    if V26_FULL_PATCH_SHA256:
        PATCH_SHA256[V26_FULL_PATCH] = V26_FULL_PATCH_SHA256


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def choose_patch(input_bytes: bytes):
    digest = sha256(input_bytes)
    if digest == V28_SHA256:
        raise BPSError("input is already the v28 release; no patch is needed")
    if digest == V27_SHA256:
        return input_bytes, PATCHES / V28_PATCH
    if digest == V26_SHA256:
        return input_bytes, PATCHES / V27_PATCH
    if digest == V25_SHA256:
        return input_bytes, PATCHES / V26_PATCH
    if digest == V24_SHA256:
        return input_bytes, PATCHES / V25_PATCH
    if digest == V23_SHA256:
        return input_bytes, PATCHES / V24_PATCH
    if digest == V22_SHA256:
        return input_bytes, PATCHES / V23_PATCH
    if digest == V21_SHA256:
        return input_bytes, PATCHES / V22_PATCH
    if digest == V20_SHA256:
        return input_bytes, PATCHES / V21_PATCH
    if digest == V19_SHA256:
        return input_bytes, PATCHES / V20_PATCH
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
    raise BPSError("input SHA-256 is not a supported original, v12 through v27 revision")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="supported original, v12 through v27 ROM")
    parser.add_argument("--out", required=True, type=Path, help="new v28 output file")
    args = parser.parse_args(argv)
    if args.out.exists():
        parser.error("refusing to overwrite existing output: {}".format(args.out))
    try:
        _require_release_metadata()
        source, patch_path = choose_patch(args.input.read_bytes())
        patch = patch_path.read_bytes()
        expected_patch = PATCH_SHA256.get(patch_path.name, "")
        if not expected_patch:
            raise BPSError("patch metadata is missing from the published release")
        if sha256(patch) != expected_patch:
            raise BPSError("patch SHA-256 does not match the published release")
        target, _ = apply_bps(source, patch)
        if patch_path.name not in (V18_PATCH, V19_PATCH, V20_PATCH, V21_PATCH, V22_PATCH, V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
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
        if patch_path.name not in (V19_PATCH, V20_PATCH, V21_PATCH, V22_PATCH, V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V18_SHA256:
                raise BPSError("intermediate ROM SHA-256 does not match v18")
            upgrade = (PATCHES / V19_PATCH).read_bytes()
            if sha256(upgrade) != PATCH_SHA256[V19_PATCH]:
                raise BPSError("v19 upgrade patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V20_PATCH, V21_PATCH, V22_PATCH, V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH) and sha256(target) != V19_SHA256:
            raise BPSError("patched ROM SHA-256 does not match the v19 release")
        if patch_path.name not in (V20_PATCH, V21_PATCH, V22_PATCH, V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            upgrade = (PATCHES / V20_PATCH).read_bytes()
            if sha256(upgrade) != PATCH_SHA256[V20_PATCH]:
                raise BPSError("v20 patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V21_PATCH, V22_PATCH, V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V20_SHA256:
                raise BPSError("patched ROM SHA-256 does not match the v20 release")
            upgrade = (PATCHES / V21_PATCH).read_bytes()
            if sha256(upgrade) != PATCH_SHA256[V21_PATCH]:
                raise BPSError("v21 patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V22_PATCH, V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V21_SHA256:
                raise BPSError("patched ROM SHA-256 does not match the v21 release")
            upgrade = (PATCHES / V22_PATCH).read_bytes()
            if sha256(upgrade) != PATCH_SHA256[V22_PATCH]:
                raise BPSError("v22 patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V23_PATCH, V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V22_SHA256:
                raise BPSError("patched ROM SHA-256 does not match the v22 release")
            upgrade=(PATCHES / V23_PATCH).read_bytes()
            if sha256(upgrade) != V23_PATCH_SHA256:
                raise BPSError("v23 patch SHA-256 does not match")
            target,_=apply_bps(target,upgrade)
        if patch_path.name not in (V24_PATCH, V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V23_SHA256:
                raise BPSError("patched ROM SHA-256 does not match the v23 release")
            upgrade = (PATCHES / V24_PATCH).read_bytes()
            if sha256(upgrade) != V24_PATCH_SHA256:
                raise BPSError("v24 patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V25_PATCH, V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V24_SHA256:
                raise BPSError("patched ROM SHA-256 does not match the v24 release")
            upgrade = (PATCHES / V25_PATCH).read_bytes()
            if sha256(upgrade) != V25_PATCH_SHA256:
                raise BPSError("v25 patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V26_PATCH, V27_PATCH, V28_PATCH):
            if sha256(target) != V25_SHA256:
                raise BPSError("patched ROM SHA-256 does not match the v25 release")
            upgrade = (PATCHES / V26_PATCH).read_bytes()
            if sha256(upgrade) != V26_PATCH_SHA256:
                raise BPSError("v26 patch SHA-256 does not match")
            target, _ = apply_bps(target, upgrade)
        if patch_path.name not in (V27_PATCH, V28_PATCH):
            if sha256(target) != V26_SHA256: raise BPSError("patched ROM SHA-256 does not match v26")
            target, _ = apply_bps(target, (PATCHES / V27_PATCH).read_bytes())
        if patch_path.name != V28_PATCH:
            if sha256(target) != V27_SHA256: raise BPSError("patched ROM SHA-256 does not match v27")
            target, _ = apply_bps(target, (PATCHES / V28_PATCH).read_bytes())
        if sha256(target) != V28_SHA256: raise BPSError("patched ROM SHA-256 does not match v28")
        # Exclusive creation keeps the no-overwrite guarantee even if another
        # process creates the destination after the check above.
        with args.out.open("xb") as output:
            output.write(target)
    except (OSError, BPSError) as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    print("Wrote {} (SHA-256: {})".format(args.out, V28_SHA256))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
