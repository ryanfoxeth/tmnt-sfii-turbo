import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parents[1];sys.path.insert(0,str(ROOT));import apply_patch
class V29Tests(unittest.TestCase):
 def test_pins_metadata_and_current_refusal(self):
  release=json.loads((ROOT/'release.json').read_text());rows={x['path']:x for x in release['patches']}
  self.assertEqual((release['version'],release['target_sha256']),('v29','03e1060d04be410d93d7a87e6668b51e6189d99ba887c526404f2c113df9001a'));self.assertEqual(set(rows),{'patches/tmnt-sfii-turbo-v29.bps','patches/tmnt-sfii-turbo-v28-to-v29.bps'})
  for name,source,pin in [('patches/tmnt-sfii-turbo-v29.bps',apply_patch.BASE_SHA256,'12696e6843d1b94039ead4e426a33d32d9ee293261fa8f3187cec898a6a1d7d3'),('patches/tmnt-sfii-turbo-v28-to-v29.bps',apply_patch.V28_SHA256,'193a288865eaa3929b30b6ad5add44978e3651141d03fd6aa985f72c07ed4f2b')]: self.assertEqual((rows[name]['source_sha256'],rows[name]['target_sha256'],hashlib.sha256((ROOT/name).read_bytes()).hexdigest()),(source,apply_patch.V29_SHA256,pin))
  with tempfile.TemporaryDirectory() as d:
   src,out=Path(d)/'in.sfc',Path(d)/'out.sfc';src.write_bytes(b'current')
   with patch.object(apply_patch,'V29_SHA256',hashlib.sha256(src.read_bytes()).hexdigest()): self.assertEqual(apply_patch.main([str(src),'--out',str(out)]),1);self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
