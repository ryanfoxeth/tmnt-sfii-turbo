"""Fail closed on unexpected public files, private paths and altered patches."""
from pathlib import Path
import hashlib
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
ALLOW={
    '.gitattributes',
    '.github/workflows/check.yml',
    '.gitignore',
    'CONTRIBUTING.md',
    'LICENSE',
    'README.md',
    'apply_patch.py',
    'art/v16/README.md',
    'art/v16/leatherhead/generation-prompts.json',
    'art/v16/leatherhead/masters/contact-000.png',
    'art/v16/leatherhead/masters/contact-024.png',
    'art/v16/leatherhead/masters/contact-048.png',
    'art/v16/leatherhead/masters/contact-072.png',
    'art/v16/leatherhead/portrait-master.png',
    'art/v16/leatherhead/portrait-prompt.json',
    'art/v16/leatherhead/templates/layout-000.json',
    'art/v16/leatherhead/templates/layout-024.json',
    'art/v16/leatherhead/templates/layout-048.json',
    'art/v16/leatherhead/templates/layout-072.json',
    'art/v16/reference-sources.json',
    'art/v16/slash/masters/contact-000.png',
    'art/v16/slash/masters/contact-024.png',
    'art/v16/slash/masters/contact-048.png',
    'art/v16/slash/masters/contact-072.png',
    'art/v16/slash/masters/contact-096.png',
    'art/v16/slash/portrait-master.png',
    'art/v16/slash/portrait-prompt.json',
    'art/v16/slash/prompts/generation-manifest.json',
    'art/v16/slash/templates/layout-000.json',
    'art/v16/slash/templates/layout-024.json',
    'art/v16/slash/templates/layout-048.json',
    'art/v16/slash/templates/layout-072.json',
    'art/v16/slash/templates/layout-096.json',
    'assets/leatherhead-slash-v16.png',
    'assets/shredder-v13.png',
    'bps.py',
    'docs/releases.md',
    'docs/technical-notes.md',
    'docs/verification.md',
    'fix_shredder_scroll_v13.py',
    'fix_stage_animation_v15.py',
    'patches/tmnt-sfii-turbo-v12-to-v13.bps',
    'patches/tmnt-sfii-turbo-v12-to-v16.bps',
    'patches/tmnt-sfii-turbo-v13-to-v16.bps',
    'patches/tmnt-sfii-turbo-v13.bps',
    'patches/tmnt-sfii-turbo-v14-to-v16.bps',
    'patches/tmnt-sfii-turbo-v15-to-v16.bps',
    'patches/tmnt-sfii-turbo-v16.bps',
    'release.json',
    'scripts/audit_public_tree.py',
    'tests/test_patcher.py',
}
PATCHES={
    'patches/tmnt-sfii-turbo-v12-to-v13.bps':'13329af6049b750b3a969c36133eb56eec7730d4ef40295b2e4b6c13c826f1e7',
    'patches/tmnt-sfii-turbo-v12-to-v16.bps':'209ee33de43780a3a6dd5ae18c5f7d209baff7cbaa1e2262eb57fe5997e1eadb',
    'patches/tmnt-sfii-turbo-v13-to-v16.bps':'d9629bf2d61c8466265791b90970212720c6db40f020cbf438c8110eff25c225',
    'patches/tmnt-sfii-turbo-v13.bps':'c2a07f402fb51e05b2c7dfadc3ea8075edaaeb57a98a56ebbb4033f476ba52fc',
    'patches/tmnt-sfii-turbo-v14-to-v16.bps':'9d72cfc01b1fc678ce4a462034f56580bafffeea61b56fdb51e57b67db6ce0e0',
    'patches/tmnt-sfii-turbo-v15-to-v16.bps':'55bf6e3e788044b2d5f2cb21388b51ddc0ee3b7c0b4489bb19af898547fb0c8b',
    'patches/tmnt-sfii-turbo-v16.bps':'86b0da6c612e31c17dc7e75e338836bce30b69a31b5634cc2fd6f1d84fb9640a',
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
