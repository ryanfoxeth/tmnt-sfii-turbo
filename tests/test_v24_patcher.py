import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch as mock_patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V24HistoryTests(unittest.TestCase):
 def test_v24_patch_files_remain_hash_pinned(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['historical_patches']}
  expected={'patches/tmnt-sfii-turbo-v24.bps':apply_patch.V24_FULL_PATCH_SHA256,
            'patches/tmnt-sfii-turbo-v23-to-v24.bps':apply_patch.V24_PATCH_SHA256}
  for path,pin in expected.items():
   self.assertIn(path,entries); self.assertEqual(entries[path]['sha256'],pin)
   self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pin)
 def test_v24_selects_v25_increment(self):
  raw=b'v24-current'
  with mock_patch.multiple(apply_patch,V24_SHA256=hashlib.sha256(raw).hexdigest(),V25_SHA256=hashlib.sha256(b'v25').hexdigest()):
   _,selected=apply_patch.choose_patch(raw); self.assertEqual(selected.name,apply_patch.V25_PATCH)
 def test_missing_v24_increment_fails_without_output(self):
  raw=b'v23-input'
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); inp,out=root/'in.sfc',root/'out.sfc'; inp.write_bytes(raw)
   with mock_patch.multiple(apply_patch,PATCHES=root,V23_SHA256=hashlib.sha256(raw).hexdigest(),V24_SHA256=hashlib.sha256(b'v24').hexdigest(),V25_SHA256=hashlib.sha256(b'v25').hexdigest(),V24_PATCH='missing-v24.bps',V24_PATCH_SHA256=hashlib.sha256(b'pin24').hexdigest(),V25_PATCH='missing-v25.bps',V25_PATCH_SHA256=hashlib.sha256(b'pin25').hexdigest()):
    self.assertEqual(apply_patch.main([str(inp),'--out',str(out)]),1); self.assertFalse(out.exists())
if __name__=='__main__': unittest.main()
