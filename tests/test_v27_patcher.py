import hashlib, json, sys, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT))
import apply_patch
class V27HistoryTests(unittest.TestCase):
 def test_v27_historical_patch_pins(self):
  release=json.loads((ROOT/'release.json').read_text()); entries={x['path']:x for x in release['historical_patches']}
  for path, expected in {'patches/tmnt-sfii-turbo-v27.bps':apply_patch.V27_FULL_PATCH_SHA256,'patches/tmnt-sfii-turbo-v26-to-v27.bps':apply_patch.V27_PATCH_SHA256}.items():
   self.assertEqual(entries[path]['sha256'],expected); self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected)
 def test_v27_selects_v28_increment(self):
  raw=b'v27 fixture'
  with patch.object(apply_patch,'V27_SHA256',hashlib.sha256(raw).hexdigest()):
   _, selected=apply_patch.choose_patch(raw); self.assertEqual(selected.name,apply_patch.V28_PATCH)
if __name__=='__main__': unittest.main()
