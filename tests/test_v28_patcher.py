import hashlib,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parents[1];sys.path.insert(0,str(ROOT));import apply_patch
class V28History(unittest.TestCase):
 def test_v28_pins_retained_and_select_v29(self):
  rows={x['path']:x for x in json.loads((ROOT/'release.json').read_text())['historical_patches']}
  for name,pin in [('patches/tmnt-sfii-turbo-v28.bps',apply_patch.V28_FULL_PATCH_SHA256),('patches/tmnt-sfii-turbo-v27-to-v28.bps',apply_patch.V28_PATCH_SHA256)]: self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),rows[name]['sha256']);self.assertEqual(rows[name]['sha256'],pin)
  raw=b'v28';
  with patch.object(apply_patch,'V28_SHA256',hashlib.sha256(raw).hexdigest()): self.assertEqual(apply_patch.choose_patch(raw)[1].name,apply_patch.V29_PATCH)
if __name__=='__main__':unittest.main()
