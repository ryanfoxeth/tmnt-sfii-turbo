"""Fail closed on unexpected public files, private paths and altered patches."""
from pathlib import Path
import hashlib
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
ALLOW={
    '.gitattributes','.gitignore','.github/workflows/check.yml',
    'README.md','LICENSE','CONTRIBUTING.md','release.json',
    'apply_patch.py','bps.py','fix_shredder_scroll_v13.py',
    'docs/releases.md','docs/technical-notes.md','docs/verification.md',
    'tests/test_patcher.py','scripts/audit_public_tree.py',
    'patches/tmnt-sfii-turbo-v13.bps','patches/tmnt-sfii-turbo-v12-to-v13.bps',
    'assets/shredder-v13.png',
}
PATCHES={
    'patches/tmnt-sfii-turbo-v13.bps':'c2a07f402fb51e05b2c7dfadc3ea8075edaaeb57a98a56ebbb4033f476ba52fc',
    'patches/tmnt-sfii-turbo-v12-to-v13.bps':'13329af6049b750b3a969c36133eb56eec7730d4ef40295b2e4b6c13c826f1e7',
}

def audit():
    if (ROOT/'.git').is_dir():
        files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
        names={x for x in files if x}
    else:
        names={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
               and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    if names!=ALLOW:
        raise ValueError(f'Public allowlist mismatch: extra={sorted(names-ALLOW)}, missing={sorted(ALLOW-names)}')
    private_markers=[b'/'+b'home'+b'/',b'/'+b'Users'+b'/',b'Dropbox'+b'/Obsidian',b'voice'+b'-note',b'@'+b'gmail.com']
    secret=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)')
    total=0
    for name in sorted(names):
        path=ROOT/name
        if path.is_symlink():raise ValueError('Symlink not permitted: '+name)
        raw=path.read_bytes();total+=len(raw)
        if name in PATCHES:
            assert raw.startswith(b'BPS1') and hashlib.sha256(raw).hexdigest()==PATCHES[name],name
        elif name.endswith('.png'):
            assert raw.startswith(b'\x89PNG\r\n\x1a\n'),name
        else:
            raw.decode('utf-8')
            assert not any(marker in raw for marker in private_markers),name
            assert not secret.search(raw),name
    print(f'Public audit passed: {len(names)} allowlisted files, {total:,} bytes; pinned BPS patches and no ROM/state files.')

if __name__=='__main__':audit()
