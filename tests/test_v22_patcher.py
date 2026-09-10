import hashlib,json,unittest
from pathlib import Path
import apply_patch
ROOT=Path(__file__).resolve().parents[1]
class ReleaseMetadataTests(unittest.TestCase):
 def test_v22_and_v23_pins_match_release_manifest_and_files(self):
  release=json.loads((ROOT/"release.json").read_text())
  self.assertEqual(apply_patch.V23_SHA256,release["target_sha256"])
  entries={x["path"]:x for x in release["patches"]}
  self.assertEqual(set(entries),{"patches/tmnt-sfii-turbo-v23.bps","patches/tmnt-sfii-turbo-v22-to-v23.bps"})
  self.assertEqual(apply_patch.V23_FULL_PATCH_SHA256,entries["patches/"+apply_patch.V23_FULL_PATCH]["sha256"])
  self.assertEqual(apply_patch.V23_PATCH_SHA256,entries["patches/"+apply_patch.V23_PATCH]["sha256"])
  for path,entry in entries.items():
   raw=(ROOT/path).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),entry["sha256"])
   self.assertEqual(apply_patch.PATCH_SHA256[path.split("/",1)[1]],entry["sha256"])
if __name__=="__main__":unittest.main()
