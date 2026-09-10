import hashlib
import struct
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch as mock_patch
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import apply_patch
from bps import BPSError, apply_bps, inspect_patch


def number(value):
    encoded = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if not value:
            encoded.append(byte | 0x80)
            return bytes(encoded)
        encoded.append(byte)
        value -= 1


def bps(source, target):
    # A compact synthetic BPS: literal target bytes plus the required CRCs.
    body = b"BPS1" + number(len(source)) + number(len(target)) + number(0)
    body += number(((len(target) - 1) << 2) | 1) + target
    body += struct.pack("<II", zlib.crc32(source) & 0xFFFFFFFF,
                        zlib.crc32(target) & 0xFFFFFFFF)
    return body + struct.pack("<I", zlib.crc32(body) & 0xFFFFFFFF)


def framed(source, target, commands):
    body = b"BPS1" + number(len(source)) + number(len(target)) + number(0)
    body += commands + struct.pack("<II", zlib.crc32(source) & 0xFFFFFFFF,
                                   zlib.crc32(target) & 0xFFFFFFFF)
    return body + struct.pack("<I", zlib.crc32(body) & 0xFFFFFFFF)


class BPSReaderTests(unittest.TestCase):
    def test_synthetic_patch_and_metrics(self):
        patch = bps(b"abcdef", b"abZdef!")
        result, info = apply_bps(b"abcdef", patch)
        self.assertEqual(result, b"abZdef!")
        self.assertEqual(info.command_counts["target_read"], 1)
        self.assertEqual(info.literal_bytes, 7)
        self.assertEqual(info.moved_source_bytes, 0)

    def test_synthetic_source_and_target_copy(self):
        # SourceCopy starts at +2 in "abcdef"; TargetCopy repeats one literal.
        source_copy = framed(b"abcdef", b"cdef", number((4 - 1) << 2 | 2) + number(4))
        result, info = apply_bps(b"abcdef", source_copy)
        self.assertEqual(result, b"cdef")
        self.assertEqual(info.moved_source_bytes, 4)

        target_copy = framed(b"", b"xxx", number(1) + b"x" + number((2 - 1) << 2 | 3) + number(0))
        self.assertEqual(apply_bps(b"", target_copy)[0], b"xxx")

    def test_corrupt_patch_crc_is_rejected(self):
        patch = bytearray(bps(b"a", b"b"))
        patch[4] = 0
        with self.assertRaises(BPSError):
            inspect_patch(bytes(patch))

    def test_valid_crc_with_invalid_copy_is_rejected(self):
        bad_source = framed(b"a", b"b", number(2) + number(4))
        bad_target = framed(b"a", b"b", number(3) + number(0))
        for patch in (bad_source, bad_target):
            with self.assertRaises(BPSError):
                inspect_patch(patch)

    def test_source_read(self):
        patch = framed(b"hello", b"hello", number((5-1) << 2))
        self.assertEqual(apply_bps(b"hello", patch)[0], b"hello")

    def test_wrong_source_is_rejected(self):
        with self.assertRaises(BPSError):
            apply_bps(b"wrong", bps(b"right", b"target"))


class CommandTests(unittest.TestCase):
    def test_supported_release_hashes_select_v16_incremental_patches(self):
        original_sha = apply_patch.sha256
        try:
            for digest, filename in apply_patch.V16_PATCHES.items():
                apply_patch.sha256 = lambda _data, digest=digest: digest
                source, patch_path = apply_patch.choose_patch(b"fixture")
                self.assertEqual(source, b"fixture")
                self.assertEqual(patch_path.name, filename)
        finally:
            apply_patch.sha256 = original_sha

    def test_headered_original_strips_copier_header_before_v16_patch(self):
        original_sha = apply_patch.sha256
        calls = iter([apply_patch.HEADERED_BASE_SHA256, apply_patch.BASE_SHA256])
        try:
            apply_patch.sha256 = lambda _data: next(calls)
            source, patch_path = apply_patch.choose_patch(b"H" * 512 + b"ROM")
            self.assertEqual(source, b"ROM")
            self.assertEqual(patch_path.name, "tmnt-sfii-turbo-v16.bps")
        finally:
            apply_patch.sha256 = original_sha

    def test_v18_upgrade_chain_and_direct_input(self):
        original, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28 = (b"original", b"v16 fixture", b"v17 fixture",
                                             b"v18 fixture", b"v19 fixture", b"v20 fixture", b"v21 fixture", b"v22 fixture", b"v23 fixture", b"v24 fixture", b"v25 fixture", b"v26 fixture", b"v27 fixture", b"v28 fixture")
        digest = lambda data: hashlib.sha256(data).hexdigest()
        first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth = (bps(original, v16), bps(v16, v17),
                                               bps(v17, v18), bps(v18, v19), bps(v19, v20), bps(v20, v21), bps(v21, v22), bps(v22, v23), bps(v23, v24), bps(v24, v25), bps(v25, v26), bps(v26, v27), bps(v27, v28))
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            for name, raw in (("first.bps", first), ("upgrade.bps", second),
                              ("v18.bps", third), ("v19.bps", fourth), ("v20.bps", fifth), ("v21.bps", sixth), ("v22.bps", seventh), ("v23.bps", eighth), ("v24.bps", ninth), ("v25.bps", tenth), ("v26.bps", eleventh), ("v27.bps", twelfth), ("v28.bps", thirteenth)):
                (directory / name).write_bytes(raw)
            with mock_patch.multiple(apply_patch, PATCHES=directory,
                    V16_SHA256=digest(v16), V17_SHA256=digest(v17), V18_SHA256=digest(v18),
                    V19_SHA256=digest(v19), V20_SHA256=digest(v20), V21_SHA256=digest(v21), V22_SHA256=digest(v22), V23_SHA256=digest(v23), V24_SHA256=digest(v24), V25_SHA256=digest(v25), V22_PATCH_SHA256=digest(seventh), V23_PATCH_SHA256=digest(eighth), V24_PATCH_SHA256=digest(ninth), V25_PATCH_SHA256=digest(tenth), V26_SHA256=digest(v26), V26_PATCH_SHA256=digest(eleventh), V27_SHA256=digest(v27), V27_PATCH_SHA256=digest(twelfth), V28_SHA256=digest(v28), V28_PATCH_SHA256=digest(thirteenth), V17_PATCH="upgrade.bps", V18_PATCH="v18.bps",
                    V19_PATCH="v19.bps", V20_PATCH="v20.bps", V21_PATCH="v21.bps", V22_PATCH="v22.bps", V23_PATCH="v23.bps", V24_PATCH="v24.bps", V25_PATCH="v25.bps", V26_PATCH="v26.bps", V27_PATCH="v27.bps", V28_PATCH="v28.bps", V16_PATCHES={digest(original): "first.bps"},
                    PATCH_SHA256={"first.bps": digest(first), "upgrade.bps": digest(second),
                                  "v18.bps": digest(third), "v19.bps": digest(fourth), "v20.bps": digest(fifth), "v21.bps": digest(sixth), "v22.bps": digest(seventh), "v23.bps": digest(eighth), "v24.bps": digest(ninth), "v25.bps": digest(tenth), "v26.bps": digest(eleventh), "v27.bps": digest(twelfth), "v28.bps": digest(thirteenth)}):
                for number, source in enumerate((original, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27)):
                    input_path = directory / f"input{number}.sfc"
                    out = directory / f"output{number}.sfc"
                    input_path.write_bytes(source)
                    self.assertEqual(apply_patch.main([str(input_path), "--out", str(out)]), 0)
                    self.assertEqual(out.read_bytes(), v28)

    def test_v18_input_selects_its_supported_upgrade(self):
        source = b"supported v18 fixture"
        with mock_patch.object(apply_patch, "V18_SHA256", hashlib.sha256(source).hexdigest()):
            normalized, selected = apply_patch.choose_patch(source)
            self.assertEqual(normalized, source)
            self.assertEqual(selected.name, apply_patch.V19_PATCH)

    def test_v20_upgrade_chain_and_direct_input(self):
        original, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28 = (b"original", b"v16 fixture", b"v17 fixture",
                                             b"v18 fixture", b"v19 fixture", b"v20 fixture", b"v21 fixture", b"v22 fixture", b"v23 fixture", b"v24 fixture", b"v25 fixture", b"v26 fixture", b"v27 fixture", b"v28 fixture")
        digest = lambda data: hashlib.sha256(data).hexdigest()
        first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth = (bps(original, v16), bps(v16, v17),
                                                bps(v17, v18), bps(v18, v19), bps(v19, v20), bps(v20, v21), bps(v21, v22), bps(v22, v23), bps(v23, v24), bps(v24, v25), bps(v25, v26), bps(v26, v27), bps(v27, v28))
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            files = {"first.bps": first, "upgrade17.bps": second,
                     "upgrade18.bps": third, "upgrade19.bps": fourth, "upgrade20.bps": fifth, "upgrade21.bps": sixth, "upgrade22.bps": seventh, "upgrade23.bps": eighth, "upgrade24.bps": ninth, "upgrade25.bps": tenth, "upgrade26.bps": eleventh, "upgrade27.bps": twelfth, "upgrade28.bps": thirteenth}
            for name, raw in files.items():
                (directory / name).write_bytes(raw)
            with mock_patch.multiple(
                    apply_patch, PATCHES=directory,
                    V16_SHA256=digest(v16), V17_SHA256=digest(v17),
                    V18_SHA256=digest(v18), V19_SHA256=digest(v19), V20_SHA256=digest(v20), V21_SHA256=digest(v21), V22_SHA256=digest(v22), V23_SHA256=digest(v23), V24_SHA256=digest(v24), V25_SHA256=digest(v25), V22_PATCH_SHA256=digest(seventh), V23_PATCH_SHA256=digest(eighth), V24_PATCH_SHA256=digest(ninth), V25_PATCH_SHA256=digest(tenth), V26_SHA256=digest(v26), V26_PATCH_SHA256=digest(eleventh), V27_SHA256=digest(v27), V27_PATCH_SHA256=digest(twelfth), V28_SHA256=digest(v28), V28_PATCH_SHA256=digest(thirteenth),
                    V17_PATCH="upgrade17.bps", V18_PATCH="upgrade18.bps",
                    V19_PATCH="upgrade19.bps", V20_PATCH="upgrade20.bps", V21_PATCH="upgrade21.bps", V22_PATCH="upgrade22.bps", V23_PATCH="upgrade23.bps", V24_PATCH="upgrade24.bps", V25_PATCH="upgrade25.bps", V26_PATCH="upgrade26.bps", V27_PATCH="upgrade27.bps", V28_PATCH="upgrade28.bps", V16_PATCHES={digest(original): "first.bps"},
                    PATCH_SHA256={name: digest(raw) for name, raw in files.items()}):
                for index, source in enumerate((original, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27)):
                    input_path = directory / f"input{index}.sfc"
                    out = directory / f"output{index}.sfc"
                    input_path.write_bytes(source)
                    self.assertEqual(apply_patch.main([str(input_path), "--out", str(out)]), 0)
                    self.assertEqual(out.read_bytes(), v28)

    def test_current_v28_input_is_reported_without_output(self):
        current = b"already current v28"
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source, out = directory / "current.sfc", directory / "out.sfc"
            source.write_bytes(current)
            with mock_patch.object(apply_patch, "V28_SHA256", hashlib.sha256(current).hexdigest()):
                with self.assertRaisesRegex(BPSError, "already the v28"):
                    apply_patch.choose_patch(current)
                self.assertEqual(apply_patch.main([str(source), "--out", str(out)]), 1)
                self.assertFalse(out.exists())

    def test_v19_corrupt_upgrade_rejected_without_output(self):
        source, target = b"v18 fixture", b"v19 fixture"
        bad = bytearray(bps(source, target)); bad[-1] ^= 1
        digest = lambda data: hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            inp, out = directory / "v18.sfc", directory / "out.sfc"
            inp.write_bytes(source); (directory / "latest.bps").write_bytes(bad)
            with mock_patch.multiple(
                    apply_patch, PATCHES=directory, V18_SHA256=digest(source),
                    V20_SHA256=digest(target), V19_PATCH="latest.bps",
                    PATCH_SHA256={"latest.bps": digest(bad)}):
                self.assertEqual(apply_patch.main([str(inp), "--out", str(out)]), 1)
                self.assertFalse(out.exists())

    def test_v18_corrupt_upgrade_rejected_without_output(self):
        source, target = b"v17 fixture", b"v18 fixture"
        bad = bytearray(bps(source, target)); bad[-1] ^= 1
        digest = lambda data: hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            inp, out = directory / "v17.sfc", directory / "out.sfc"
            inp.write_bytes(source); (directory / "latest.bps").write_bytes(bad)
            with mock_patch.multiple(apply_patch, PATCHES=directory,
                    V17_SHA256=digest(source), V18_SHA256=digest(target), V18_PATCH="latest.bps",
                    PATCH_SHA256={"latest.bps": digest(bad)}):
                self.assertEqual(apply_patch.main([str(inp), "--out", str(out)]), 1)
                self.assertFalse(out.exists())

    def test_unexpected_intermediate_is_rejected_before_upgrade(self):
        source, intermediate = b"source", b"unexpected intermediate"
        digest = lambda data: hashlib.sha256(data).hexdigest()
        first = bps(source, intermediate)
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            input_path, out = directory / "input.sfc", directory / "output.sfc"
            input_path.write_bytes(source)
            (directory / "first.bps").write_bytes(first)
            with mock_patch.multiple(apply_patch, PATCHES=directory,
                    V16_SHA256=digest(b"expected intermediate"),
                    V16_PATCHES={digest(source): "first.bps"},
                    PATCH_SHA256={"first.bps": digest(first)}):
                self.assertEqual(apply_patch.main([str(input_path), "--out", str(out)]), 1)
                self.assertFalse(out.exists())

    def test_v22_missing_incremental_pin_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source, out = directory / "v21.sfc", directory / "out.sfc"
            source.write_bytes(b"recognized-v21")
            with mock_patch.multiple(apply_patch, V21_SHA256=hashlib.sha256(source.read_bytes()).hexdigest(), V22_PATCH_SHA256=None):
                self.assertEqual(apply_patch.main([str(source), "--out", str(out)]), 1)
                self.assertFalse(out.exists())

    def test_wrong_revision_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            input_path = directory / "wrong.sfc"
            out = directory / "out.sfc"
            input_path.write_bytes(b"wrong")
            self.assertEqual(apply_patch.main([str(input_path), "--out", str(out)]), 1)
            self.assertFalse(out.exists())

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            input_path = directory / "input.sfc"
            out = directory / "out.sfc"
            input_path.write_bytes(b"anything")
            out.write_bytes(b"keep")
            with self.assertRaises(SystemExit):
                apply_patch.main([str(input_path), "--out", str(out)])
            self.assertEqual(out.read_bytes(), b"keep")



class V28ChainTests(unittest.TestCase):
    def test_full_synthetic_chain_through_v28(self):
        original, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28 = (
            b"original", b"v16 fixture", b"v17 fixture", b"v18 fixture",
            b"v19 fixture", b"v20 fixture", b"v21 fixture", b"v22 fixture",
            b"v23 fixture", b"v24 fixture", b"v25 fixture", b"v26 fixture", b"v27 fixture", b"v28 fixture")
        values = (original, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28)
        names = ("first.bps", "upgrade17.bps", "upgrade18.bps", "upgrade19.bps",
                 "upgrade20.bps", "upgrade21.bps", "upgrade22.bps", "upgrade23.bps",
                 "upgrade24.bps", "upgrade25.bps", "upgrade26.bps", "upgrade27.bps", "upgrade28.bps")
        patches = {name: bps(values[i], values[i + 1]) for i, name in enumerate(names)}
        digest = lambda data: hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            for name, raw in patches.items():
                (directory / name).write_bytes(raw)
            with mock_patch.multiple(
                    apply_patch, PATCHES=directory,
                    V16_SHA256=digest(v16), V17_SHA256=digest(v17),
                    V18_SHA256=digest(v18), V19_SHA256=digest(v19),
                    V20_SHA256=digest(v20), V21_SHA256=digest(v21),
                    V22_SHA256=digest(v22), V23_SHA256=digest(v23),
                    V24_SHA256=digest(v24), V25_SHA256=digest(v25),
                    V26_SHA256=digest(v26), V27_SHA256=digest(v27), V28_SHA256=digest(v28), V22_PATCH_SHA256=digest(patches["upgrade22.bps"]),
                    V23_PATCH_SHA256=digest(patches["upgrade23.bps"]),
                    V24_PATCH_SHA256=digest(patches["upgrade24.bps"]),
                    V25_PATCH_SHA256=digest(patches["upgrade25.bps"]),
                    V26_PATCH_SHA256=digest(patches["upgrade26.bps"]), V27_PATCH_SHA256=digest(patches["upgrade27.bps"]), V28_PATCH_SHA256=digest(patches["upgrade28.bps"]),
                    V17_PATCH="upgrade17.bps", V18_PATCH="upgrade18.bps",
                    V19_PATCH="upgrade19.bps", V20_PATCH="upgrade20.bps",
                    V21_PATCH="upgrade21.bps", V22_PATCH="upgrade22.bps",
                    V23_PATCH="upgrade23.bps", V24_PATCH="upgrade24.bps",
                    V25_PATCH="upgrade25.bps", V26_PATCH="upgrade26.bps", V27_PATCH="upgrade27.bps", V28_PATCH="upgrade28.bps",
                    V16_PATCHES={digest(original): "first.bps"},
                    PATCH_SHA256={name: digest(raw) for name, raw in patches.items()}):
                for index, source in enumerate(values[:-1]):
                    inp = directory / f"input{index}.sfc"
                    out = directory / f"output{index}.sfc"
                    inp.write_bytes(source)
                    self.assertEqual(apply_patch.main([str(inp), "--out", str(out)]), 0)
                    self.assertEqual(out.read_bytes(), v28)

    def test_missing_v26_increment_fails_without_output(self):
        source = b"recognized-v25"
        digest = hashlib.sha256(source).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            inp, out = directory / "v25.sfc", directory / "out.sfc"
            inp.write_bytes(source)
            with mock_patch.multiple(apply_patch, V25_SHA256=digest,
                                     V26_PATCH_SHA256=None):
                self.assertEqual(apply_patch.main([str(inp), "--out", str(out)]), 1)
                self.assertFalse(out.exists())

if __name__ == "__main__":
    unittest.main()
