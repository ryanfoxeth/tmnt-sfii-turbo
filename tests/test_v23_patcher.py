import hashlib,sys,tempfile,unittest
from unittest.mock import patch as mock_patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
import apply_patch
class V23Tests(unittest.TestCase):
 def test_current_v23_rejected_without_output(self):
  raw=b'v23-current'; old=apply_patch.V23_SHA256; apply_patch.V23_SHA256=hashlib.sha256(raw).hexdigest()
  try:
   with tempfile.TemporaryDirectory() as d:
    i,o=Path(d)/'i.sfc',Path(d)/'o.sfc';i.write_bytes(raw);self.assertEqual(apply_patch.main([str(i),'--out',str(o)]),1);self.assertFalse(o.exists())
  finally: apply_patch.V23_SHA256=old

 def test_missing_v22_to_v23_increment_fails_without_output(self):
  source=b'v22 fixture'
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); inp,out=root/'v22.sfc',root/'out.sfc';inp.write_bytes(source)
   with mock_patch.multiple(apply_patch, PATCHES=root, V22_SHA256=hashlib.sha256(source).hexdigest(),
                            V23_SHA256=hashlib.sha256(b'v23 fixture').hexdigest(),
                            V23_PATCH='missing-v22-to-v23.bps', V23_PATCH_SHA256=hashlib.sha256(b'pinned patch').hexdigest()):
    self.assertEqual(apply_patch.main([str(inp),'--out',str(out)]),1)
    self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
