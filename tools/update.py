#!/usr/bin/env python3
"""Regenerate Packages / Release for the flat APT (Cydia) repo in docs/.
Usage: python3 tools/update.py   (after adding .deb files to docs/debs/)"""
import bz2, gzip, hashlib, io, os, subprocess, tarfile, time
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
BASE = 'https://nmt3325.github.io/nmt3325/'
EXTRA = {  # per-package extra Packages fields
    'dev.owngoal.icli6': {'Author': 'nmt3325', 'Homepage': 'https://github.com/nmt3325/icli6',
                          'Depiction': BASE + 'depictions/icli6.html'},
}
def ar_members(path):
    with open(path, 'rb') as f:
        assert f.read(8) == b'!<arch>\n'
        while True:
            h = f.read(60)
            if len(h) < 60: break
            name = h[:16].decode().strip().rstrip('/'); size = int(h[48:58])
            data = f.read(size); f.read(size & 1)
            yield name, data
def control_of(path):
    for name, data in ar_members(path):
        if name.startswith('control.tar'):
            mode = 'r:gz' if name.endswith('gz') else 'r:xz' if name.endswith('xz') else 'r:*'
            with tarfile.open(fileobj=io.BytesIO(data), mode=mode) as t:
                for m in t.getmembers():
                    if m.name.lstrip('./') == 'control':
                        return t.extractfile(m).read().decode()
    raise SystemExit('no control in ' + path)
entries = []
for fn in sorted(os.listdir(os.path.join(ROOT, 'debs'))):
    if not fn.endswith('.deb'): continue
    p = os.path.join(ROOT, 'debs', fn); raw = open(p, 'rb').read()
    ctl = control_of(p).strip()
    pkg = [l.split(':', 1)[1].strip() for l in ctl.splitlines() if l.startswith('Package:')][0]
    keys = {l.split(':', 1)[0] for l in ctl.splitlines() if ':' in l and not l.startswith(' ')}
    for k, v in EXTRA.get(pkg, {}).items():
        if k not in keys: ctl += f'\n{k}: {v}'
    ctl += (f'\nFilename: debs/{fn}\nSize: {len(raw)}\nMD5sum: {hashlib.md5(raw).hexdigest()}'
            f'\nSHA1: {hashlib.sha1(raw).hexdigest()}\nSHA256: {hashlib.sha256(raw).hexdigest()}')
    entries.append(ctl)
pk = ('\n\n'.join(entries) + '\n').encode()
files = {'Packages': pk, 'Packages.bz2': bz2.compress(pk), 'Packages.gz': gzip.compress(pk, mtime=0)}
for n, d in files.items(): open(os.path.join(ROOT, n), 'wb').write(d)
rel = ['Origin: nmt3325 Repository', 'Label: nmt3325 Repository', 'Suite: stable', 'Version: 1.0', 'Codename: ios',
       'Architectures: iphoneos-arm', 'Components: main', 'Description: nmt3325 の Cydia リポジトリ (iOS 6 対応ツールなど)',
       'Date: ' + time.strftime('%a, %d %b %Y %H:%M:%S UTC', time.gmtime())]
for algo, h in (('MD5Sum', hashlib.md5), ('SHA1', hashlib.sha1), ('SHA256', hashlib.sha256)):
    rel.append(algo + ':')
    for n, d in files.items(): rel.append(f' {h(d).hexdigest()} {len(d)} {n}')
open(os.path.join(ROOT, 'Release'), 'w').write('\n'.join(rel) + '\n')
print(f'{len(entries)} package(s)')
