import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch as mock_patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V24Tests(unittest.TestCase):
 def test_v24_metadata_matches_release_and_patch_files(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['patches']}
  self.assertEqual(release['target_sha256'],apply_patch.V24_SHA256)
  self.assertEqual(set(entries),{'patches/tmnt-sfii-turbo-v24.bps','patches/tmnt-sfii-turbo-v23-to-v24.bps'})
  for path,entry in entries.items(): self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),entry['sha256'])
 def test_current_v24_is_rejected_without_output(self):
  raw=b'v24-current'
  with tempfile.TemporaryDirectory() as d, mock_patch.object(apply_patch,'V24_SHA256',hashlib.sha256(raw).hexdigest()):
   inp,out=Path(d)/'in.sfc',Path(d)/'out.sfc'; inp.write_bytes(raw)
   self.assertEqual(apply_patch.main([str(inp),'--out',str(out)]),1); self.assertFalse(out.exists())
 def test_missing_v24_increment_fails_without_output(self):
  raw=b'v23-input'
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); inp,out=root/'in.sfc',root/'out.sfc'; inp.write_bytes(raw)
   with mock_patch.multiple(apply_patch,PATCHES=root,V23_SHA256=hashlib.sha256(raw).hexdigest(),V24_SHA256=hashlib.sha256(b'v24').hexdigest(),V24_PATCH='missing.bps',V24_PATCH_SHA256=hashlib.sha256(b'pin').hexdigest()):
    self.assertEqual(apply_patch.main([str(inp),'--out',str(out)]),1); self.assertFalse(out.exists())
if __name__=='__main__': unittest.main()
