import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch as mock_patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V23HistoryTests(unittest.TestCase):
 def test_v23_patch_files_remain_hash_pinned(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['historical_patches']}
  expected={'patches/tmnt-sfii-turbo-v23.bps':apply_patch.V23_FULL_PATCH_SHA256,
            'patches/tmnt-sfii-turbo-v22-to-v23.bps':apply_patch.V23_PATCH_SHA256}
  for path,pin in expected.items():
   self.assertIn(path,entries); self.assertEqual(entries[path]['sha256'],pin)
   self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pin)
 def test_v23_selects_v24_increment(self):
  raw=b'v23-current'
  with mock_patch.multiple(apply_patch,V23_SHA256=hashlib.sha256(raw).hexdigest(),V24_SHA256=hashlib.sha256(b'v24').hexdigest()):
   _,selected=apply_patch.choose_patch(raw); self.assertEqual(selected.name,apply_patch.V24_PATCH)
 def test_missing_v23_increment_fails_without_output(self):
  raw=b'v22-input'
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); inp,out=root/'in.sfc',root/'out.sfc'; inp.write_bytes(raw)
   with mock_patch.multiple(apply_patch,PATCHES=root,V22_SHA256=hashlib.sha256(raw).hexdigest(),V23_SHA256=hashlib.sha256(b'v23').hexdigest(),V24_SHA256=hashlib.sha256(b'v24').hexdigest(),V23_PATCH='missing-v22-to-v23.bps',V23_PATCH_SHA256=hashlib.sha256(b'pin23').hexdigest()):
    self.assertEqual(apply_patch.main([str(inp),'--out',str(out)]),1); self.assertFalse(out.exists())
if __name__=='__main__': unittest.main()
