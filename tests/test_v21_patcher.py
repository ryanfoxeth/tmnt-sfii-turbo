import hashlib
import tempfile
import unittest
from pathlib import Path

import apply_patch


class V21PatcherTests(unittest.TestCase):
    def test_v21_patch_pin_and_current_rejection(self):
        patch_path = apply_patch.PATCHES / apply_patch.V21_PATCH
        self.assertEqual(hashlib.sha256(patch_path.read_bytes()).hexdigest(),
                         apply_patch.PATCH_SHA256[apply_patch.V21_PATCH])
        self.assertEqual(apply_patch.V21_SHA256,
                         "27bab79c6cf21c284f9aa52d396088cdc8f1d8bd7983683d1e51e1a826dc8671")

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "current.sfc"
            output = Path(directory) / "output.sfc"
            source.write_bytes(b"synthetic-current-v21")
            old = apply_patch.V21_SHA256
            apply_patch.V21_SHA256 = hashlib.sha256(source.read_bytes()).hexdigest()
            try:
                self.assertEqual(apply_patch.main([str(source), "--out", str(output)]), 1)
                self.assertFalse(output.exists())
            finally:
                apply_patch.V21_SHA256 = old


if __name__ == "__main__":
    unittest.main()
