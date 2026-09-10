import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V27Tests(unittest.TestCase):
 def test_current_metadata_and_patch_hashes(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['patches']}
  self.assertEqual(release['target_sha256'],apply_patch.V27_SHA256)
  self.assertEqual(set(entries),{'patches/tmnt-sfii-turbo-v27.bps','patches/tmnt-sfii-turbo-v26-to-v27.bps'})
  for path,row in entries.items(): self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),row['sha256'])
 def test_current_v27_refuses_without_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); source,out=root/'in.sfc',root/'out.sfc'; source.write_bytes(b'current-v27')
   with patch.object(apply_patch,'V27_SHA256',hashlib.sha256(source.read_bytes()).hexdigest()):
    self.assertEqual(apply_patch.main([str(source),'--out',str(out)]),1); self.assertFalse(out.exists())
if __name__=='__main__': unittest.main()
