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
    'tests/test_v22_patcher.py',
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
ALLOW.update({'patches/tmnt-sfii-turbo-v17.bps', 'art/v17/geometry-review.json', 'art/v17/README.md', 'patches/tmnt-sfii-turbo-v16-to-v17.bps', 'assets/consistency-v17.png'})
PATCHES.update({'patches/tmnt-sfii-turbo-v17.bps': '41272fcffd6785b504df73494ab6b3c903f320f94a6b5e5cc9598dd89562266c', 'patches/tmnt-sfii-turbo-v16-to-v17.bps': '5e26d62d89066ae89f606671582b16b661e90edbe6bd38ef6620f08457ef0a04'})

ALLOW.update({'patches/tmnt-sfii-turbo-v18.bps', 'patches/tmnt-sfii-turbo-v17-to-v18.bps'})
PATCHES.update({'patches/tmnt-sfii-turbo-v18.bps': '4a4be276c845b43b9e9a36ee09ffbbc198233f8f8b89d81acf85de76c546e86f', 'patches/tmnt-sfii-turbo-v17-to-v18.bps': '3a4b815ec4ec1aa54e805a3bf11a145825ad92b46d4296c48576272ea381f5a6'})
ALLOW.update({'assets/select-v18.png','assets/cleanup-v18.png'})
ALLOW.update({'patches/tmnt-sfii-turbo-v19.bps', 'patches/tmnt-sfii-turbo-v18-to-v19.bps'})
PATCHES.update({'patches/tmnt-sfii-turbo-v19.bps': '055c3ae7aa0fcb99b59a6661e875774702229e17a52a538a168874e8addd2db9', 'patches/tmnt-sfii-turbo-v18-to-v19.bps': '46902d9035ec1d65e3335ae56329938bc18bac16650344d7b6af061a47f9f34b'})
ALLOW.update({'patches/tmnt-sfii-turbo-v19-to-v20.bps', 'patches/tmnt-sfii-turbo-v20.bps'})
PATCHES.update({'patches/tmnt-sfii-turbo-v20.bps': '3c8e8488017b868099ad1e3511baedb1a6ec9e57ee65a3189349b83646cab481', 'patches/tmnt-sfii-turbo-v19-to-v20.bps': '771c9269a7a463267118b96ab2001996d651a730adc10156dd710fef5b60f86c'})
ALLOW.update({'patches/tmnt-sfii-turbo-v21.bps', 'patches/tmnt-sfii-turbo-v20-to-v21.bps'})
PATCHES.update({'patches/tmnt-sfii-turbo-v21.bps': 'd13799cb9ba4d491eb9f6c02e22bca2d26421e6e5993f98f92db4a698b3a16cf', 'patches/tmnt-sfii-turbo-v20-to-v21.bps': '37c53fbf8a8b49a44acc2ae70c053ef5a1d912c7e9da209a60e4f35e96856e36'})


ALLOW.add('assets/alt-turtles-v21.png')
# Verified v22 full and incremental BPS artifacts.
ALLOW.update({'patches/tmnt-sfii-turbo-v22.bps','patches/tmnt-sfii-turbo-v21-to-v22.bps'})
PATCHES.update({'patches/tmnt-sfii-turbo-v22.bps':'54498426698c7d35ceb347642a4c322784e01d4e5a8f3b5c2a9a93a583a5f437','patches/tmnt-sfii-turbo-v21-to-v22.bps':'bcd2dba4823b5327917c281b5206c5a2669562da981a94f136c36faaae08bb3e'})

ALLOW.update({'patches/tmnt-sfii-turbo-v23.bps','patches/tmnt-sfii-turbo-v22-to-v23.bps','tests/test_v23_patcher.py','assets/endings-v23.png'})
PATCHES.update({'patches/tmnt-sfii-turbo-v23.bps': '4df54d5cffe9acbb1370278a34120d7926bd09b180d7e0ce835827e47052e6f5', 'patches/tmnt-sfii-turbo-v22-to-v23.bps': '27519ca0023ccafcda6a3d7a39b62d4f6ede9152f86298d5ff44318ec438519b'})

# Private v24 staging additions.
ALLOW.update({'patches/tmnt-sfii-turbo-v24.bps','patches/tmnt-sfii-turbo-v23-to-v24.bps','tests/test_v24_patcher.py'})
PATCHES.update({'patches/tmnt-sfii-turbo-v24.bps': '82692fca5805e9a6fac7962424591c82d98d8b5a51262f0b7c6929b032b71b35','patches/tmnt-sfii-turbo-v23-to-v24.bps': '17f46bf12b21a657584bb7c208b845eeb27c88af8d16ab26f6abc3673e351e6a'})

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
