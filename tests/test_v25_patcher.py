import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V25Tests(unittest.TestCase):
 def test_latest_metadata_and_patch_files(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['patches']}
  self.assertEqual(release['target_sha256'],apply_patch.V25_SHA256)
  self.assertEqual(set(entries),{'patches/tmnt-sfii-turbo-v25.bps','patches/tmnt-sfii-turbo-v24-to-v25.bps'})
  for path,row in entries.items(): self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),row['sha256'])
 def test_current_v25_and_missing_increment_leave_no_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); source,out=root/'in.sfc',root/'out.sfc'; current=b'current-v25'; source.write_bytes(current)
   with patch.object(apply_patch,'V25_SHA256',hashlib.sha256(current).hexdigest()):
    self.assertEqual(apply_patch.main([str(source),'--out',str(out)]),1); self.assertFalse(out.exists())
   with patch.multiple(apply_patch,PATCHES=root,V24_SHA256=hashlib.sha256(current).hexdigest(),V25_SHA256=hashlib.sha256(b'next').hexdigest(),V25_PATCH='missing.bps',V25_PATCH_SHA256=hashlib.sha256(b'pin').hexdigest()):
    self.assertEqual(apply_patch.main([str(source),'--out',str(out)]),1); self.assertFalse(out.exists())
if __name__=='__main__': unittest.main()
