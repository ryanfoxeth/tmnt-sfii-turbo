import hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch as mock_patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V22HistoryTests(unittest.TestCase):
 def test_v22_patch_files_remain_hash_pinned(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['historical_patches']}
  expected={'patches/tmnt-sfii-turbo-v22.bps':apply_patch.V22_FULL_PATCH_SHA256,
            'patches/tmnt-sfii-turbo-v21-to-v22.bps':apply_patch.V22_PATCH_SHA256}
  for path,pin in expected.items():
   self.assertIn(path,entries); self.assertEqual(entries[path]['sha256'],pin)
   self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pin)
 def test_v22_selects_v23_increment(self):
  raw=b'v22-current'
  with mock_patch.multiple(apply_patch,V22_SHA256=hashlib.sha256(raw).hexdigest(),V23_SHA256=hashlib.sha256(b'v23').hexdigest()):
   _,selected=apply_patch.choose_patch(raw); self.assertEqual(selected.name,apply_patch.V23_PATCH)
 def test_missing_v22_increment_fails_without_output(self):
  raw=b'v21-input'
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); inp,out=root/'in.sfc',root/'out.sfc'; inp.write_bytes(raw)
   with mock_patch.multiple(apply_patch,PATCHES=root,V21_SHA256=hashlib.sha256(raw).hexdigest(),V22_SHA256=hashlib.sha256(b'v22').hexdigest(),V23_SHA256=hashlib.sha256(b'v23').hexdigest(),V22_PATCH='missing-v21-to-v22.bps',V22_PATCH_SHA256=hashlib.sha256(b'pin22').hexdigest()):
    self.assertEqual(apply_patch.main([str(inp),'--out',str(out)]),1); self.assertFalse(out.exists())
if __name__=='__main__': unittest.main()
