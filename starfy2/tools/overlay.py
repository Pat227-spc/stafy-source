#!/usr/bin/env python3
"""Overlay script/fix trees onto the scratch build tree (never onto repo/).
usage: overlay.py TREE BAT MANIFEST SRC:DESTPREFIX [SRC:DESTPREFIX ...]   (later sources win)
  backfill/scripts:asm/bin/text   -> files mirror asm/bin/text/
  overlay:.                       -> files mirror the repo root (TBLs, asm/, asm/bin/text/...)
Paths are matched case-insensitively against existing files and dirs (NTFS semantics), so an overlay
replaces the upstream file rather than creating a case-variant twin.
MANIFEST (TSV): kind  tree_relpath  src_path  pointers
  kind = replace  (file existed upstream: rides the normal assemble.bat steps)
       | scene    (a NEW .txt under asm/bin/text not run by assemble.bat: gets import.bin reset, Atlas, lzss and is
                   linked by tools/overlay asm via its pointers)
       | other    (new non-script file, copied only)
Pointers for a new scene come from a header comment in the .txt, `//POINTER: 0x0814E2C8 0x082C2660`
(Atlas ignores // lines), or from a `scenes.tsv` in the overlay root: `relpath<TAB>0xPTR[ 0xPTR...]`.
Files under Uncompressed/Blocks/ are never scenes (they are concatenated into Uncompressed_Text.txt)."""
import sys, os, re, shutil
tree, bat, manifest = sys.argv[1], sys.argv[2], sys.argv[3]
def ci_resolve(base, rel, create_dirs=False):
    cur = base; parts = rel.replace('\\', '/').split('/')
    for i, p in enumerate(parts):
        cand = os.path.join(cur, p)
        if not os.path.exists(cand) and os.path.isdir(cur):
            m = [e for e in os.listdir(cur) if e.lower() == p.lower()]
            if m: cand = os.path.join(cur, m[0])
        cur = cand
    return os.path.relpath(cur, base)
# scripts that assemble.bat already runs through Atlas (lower-cased tree paths)
batscripts = set()
for line in open(bat, encoding='latin-1'):
    w = line.split()
    if len(w) == 3 and w[0].lower() == 'atlas': batscripts.add(w[2].replace('\\', '/').lower())
rows = []
for spec in sys.argv[4:]:
    src, dest = spec.rsplit(':', 1)
    if not os.path.isdir(src): continue
    side = {}
    st = os.path.join(src, 'scenes.tsv')
    if os.path.exists(st):
        for l in open(st, encoding='utf-8'):
            if l.strip() and not l.startswith('#'):
                a, _, b = l.rstrip('\n').partition('\t'); side[a.strip().replace('\\', '/').lower()] = b.split()
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not (root == src and d == 'glyphs')]
        for f in sorted(files):
            if f.startswith('.') or f in ('scenes.tsv', 'README.md') and root == src: continue
            sp = os.path.join(root, f); rel = os.path.normpath(os.path.join(dest, os.path.relpath(sp, src))).replace('\\', '/')
            trel = ci_resolve(tree, rel).replace('\\', '/')
            existed = os.path.exists(os.path.join(tree, trel))
            os.makedirs(os.path.dirname(os.path.join(tree, trel)) or '.', exist_ok=True)
            shutil.copyfile(sp, os.path.join(tree, trel))
            low = trel.lower(); ptrs = []
            if low.endswith('.txt') and low.startswith('asm/bin/text/') and '/uncompressed/' not in low and low not in batscripts:
                kind = 'scene'
                head = open(sp, 'rb').read(4096).decode('latin-1')
                for m in re.finditer(r'(?im)^//\s*POINTERS?\s*:\s*(.+)$', head): ptrs += re.findall(r'0x[0-9A-Fa-f]{7,8}|\$[0-9A-Fa-f]{7,8}', m.group(1))
                ptrs += side.get(os.path.relpath(sp, src).replace('\\', '/').lower(), [])
                ptrs = ['0x' + p.lstrip('$').replace('0x', '').upper() for p in ptrs]
            else:
                kind = 'replace' if existed else 'other'
            rows.append((kind, trel, sp, ' '.join(dict.fromkeys(ptrs))))
with open(manifest, 'w') as o:
    for r in rows: o.write('\t'.join(r) + '\n')
from collections import Counter
print('overlay: %d files (%s)' % (len(rows), ', '.join('%s=%d' % kv for kv in Counter(r[0] for r in rows).items()) or 'none'))
