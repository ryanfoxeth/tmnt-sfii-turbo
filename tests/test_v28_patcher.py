import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parents[1];sys.path.insert(0,str(ROOT))
import apply_patch
class V28Tests(unittest.TestCase):
 def test_current_bps_pins_and_source_bounds(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['patches']}
  self.assertEqual(release['target_sha256'],apply_patch.V28_SHA256);self.assertEqual(release['checksum'],'F1F0')
  self.assertEqual(release['source_release'],{'version':'v27','sha256':apply_patch.V27_SHA256})
  expected={'patches/tmnt-sfii-turbo-v28.bps':(apply_patch.BASE_SHA256,apply_patch.V28_SHA256,apply_patch.V28_FULL_PATCH_SHA256),'patches/tmnt-sfii-turbo-v27-to-v28.bps':(apply_patch.V27_SHA256,apply_patch.V28_SHA256,apply_patch.V28_PATCH_SHA256)}
  self.assertEqual(set(entries),set(expected))
  for path,(source,target,pin) in expected.items():
   row=entries[path];self.assertEqual((row['source_sha256'],row['target_sha256'],row['sha256']),(source,target,pin));self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pin)
 def test_current_v28_refuses_without_output(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);src,out=d/'in.sfc',d/'out.sfc';src.write_bytes(b'current-v28')
   with patch.object(apply_patch,'V28_SHA256',hashlib.sha256(src.read_bytes()).hexdigest()):
    self.assertEqual(apply_patch.main([str(src),'--out',str(out)]),1);self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
