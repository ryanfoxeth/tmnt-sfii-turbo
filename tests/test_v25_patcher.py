import hashlib, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V25HistoryTests(unittest.TestCase):
 def test_v25_is_retained_as_historical_pins(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['historical_patches']}
  for path,pin in [('patches/tmnt-sfii-turbo-v25.bps',apply_patch.V25_FULL_PATCH_SHA256),('patches/tmnt-sfii-turbo-v24-to-v25.bps',apply_patch.V25_PATCH_SHA256)]:
   self.assertIn(path,entries); self.assertEqual(entries[path]['sha256'],pin); self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pin)
 def test_v25_selects_v26_increment(self):
  raw=b'v25 fixture'; original=apply_patch.V25_SHA256
  try:
   apply_patch.V25_SHA256=hashlib.sha256(raw).hexdigest(); _,selected=apply_patch.choose_patch(raw); self.assertEqual(selected.name,apply_patch.V26_PATCH)
  finally: apply_patch.V25_SHA256=original
if __name__=='__main__': unittest.main()
