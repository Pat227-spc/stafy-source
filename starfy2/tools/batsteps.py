#!/usr/bin/env python3
"""Parse the upstream assemble.bat into resolved Linux build steps (TSV on stdout).
Paths are resolved case-insensitively against TREE (NTFS semantics). Steps:
  import<TAB>dest            (copy asm/bin/text/import.bin over dest)
  atlas<TAB>target<TAB>script
  lzss<TAB>file [file...]    (one line per bat line, wildcards expanded)
  armips<TAB>file.asm        (only non-commented lines)
Unknown lines are reported on stderr so upstream changes are noticed."""
import sys, os, fnmatch
tree, bat = sys.argv[1], sys.argv[2]
def resolve(rel, base=tree, must=True):
    parts = rel.replace('\\', '/').split('/'); cur = base
    for i, p in enumerate(parts):
        if p in ('', '.'): continue
        if p == '..': cur = os.path.dirname(cur); continue
        cand = os.path.join(cur, p)
        if not os.path.exists(cand):
            m = [e for e in os.listdir(cur) if e.lower() == p.lower()] if os.path.isdir(cur) else []
            if m: cand = os.path.join(cur, m[0])
            elif must or i < len(parts) - 1:
                sys.stderr.write(f"MISSING: {rel}\n"); return None
        cur = cand
    return os.path.relpath(cur, tree)
def glob_ci(rel):
    d, pat = os.path.split(rel.replace('\\', '/'))
    rd = resolve(d) if d else '.'
    if rd is None: return []
    full = os.path.join(tree, rd)
    return sorted((os.path.join(rd, e) for e in os.listdir(full) if fnmatch.fnmatch(e.lower(), pat.lower())), key=str.upper)
textdir = 'asm/bin/text'
known_other = {'echo on', 'pause', 'cd rom', 'cd..', 'cd asm\\bin\\text', 'cd..\\..\\..', 'cd..\\', 'cd..\\..\\..\\..\\',
               'copy input.gba output.gba', 'copy /b output.gba+padding.bin output.gba', 'move blocks\\uncompressed_text.txt',
               'cd asm\\bin\\text\\uncompressed\\blocks', 'copy first\\first.txt+*.txt uncompressed_text.txt',
               'flips --apply asm\\vwf\\vwf.bps rom\\output.gba'}
for raw in open(bat, encoding='latin-1'):
    line = raw.strip()
    if not line or line.startswith('::'): continue
    w = line.split(); cmd = w[0].lower()
    if cmd == 'copy' and len(w) == 3 and w[1].lower() == 'import.bin':
        r = resolve(textdir + '/' + w[2], must=False)
        if r: print(f"import\t{r}")
    elif cmd == 'atlas' and len(w) == 3:
        t, s = resolve(w[1], must=False), resolve(w[2])
        if t and s: print(f"atlas\t{t}\t{s}")
    elif cmd == 'lzss' and w[1] == '-ewo':
        files = []
        for a in w[2:]: files += glob_ci(a) if '*' in a else [x for x in [resolve(a)] if x]
        if files: print("lzss\t" + "\t".join(files))
        else: sys.stderr.write(f"NOFILES: {line}\n")
    elif cmd == 'armips':
        r = resolve(w[1])
        if r: print(f"armips\t{r}")
    elif line.lower().rstrip('\\') + ('\\' if line.endswith('\\') else '') in known_other or line.lower() in known_other:
        pass
    else:
        sys.stderr.write(f"UNHANDLED: {line}\n")
