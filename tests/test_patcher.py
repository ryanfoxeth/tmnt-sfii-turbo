import hashlib
import struct
import sys
from pathlib import Path
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
