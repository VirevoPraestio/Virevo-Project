"""Tojo v2 — point-index lint.

The point index is the layer below the chunks: every individually named question,
KPI, parameter, dependency and consideration in the library, with the chunk it
lives in. It is searched by the retriever and never enters the prompt, so the
failure it has to be protected from is not size — it is pointing somewhere wrong.

    python3 lint_points.py --points <dir> --refs <dir>

Exits non-zero on any error. Warnings do not fail the build.
"""

import argparse
import glob
import os
import re
import sys

CHUNK_RE = re.compile(r"<!--chunk\s*\n(.*?)\n-->", re.S)
ROW_RE = re.compile(r"^\|\s*([a-z]+\.[\w.\-]+#\w+)\s*\|(.*?)\|(.*?)\|(.*?)\|\s*$")
POINT_RE = re.compile(r"^([a-z]+\.[\w.\-]+)#([a-z])(\d+)$")
KINDS = set("qkpdcfnxas")
MAX_WORDS = 12


def load_chunks(refs):
    """chunk id -> (file, retrievable?)"""
    out = {}
    for path in sorted(glob.glob(os.path.join(refs, "*.md"))):
        for m in CHUNK_RE.finditer(open(path).read()):
            f = {}
            for line in m.group(1).split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    f[k.strip()] = v.strip()
            if "id" in f:
                out[f["id"]] = (os.path.basename(path),
                                f.get("retrieve") != "never")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", required=True)
    ap.add_argument("--refs", required=True)
    a = ap.parse_args()

    chunks = load_chunks(a.refs)
    if not chunks:
        print("ERROR no chunks found — is --refs right?")
        return 1

    errors, warnings = [], []
    seen, per_chunk, per_kind, no_alias = {}, {}, {}, 0
    files = {}

    for path in sorted(glob.glob(os.path.join(a.points, "*.points.md"))):
        name = os.path.basename(path)
        n = 0
        for lineno, line in enumerate(open(path), 1):
            m = ROW_RE.match(line.rstrip())
            if not m:
                continue
            pid, what, chunk, alias = (x.strip() for x in m.groups())
            if pid in ("point",) or set(pid) <= set("-| "):
                continue
            n += 1

            pm = POINT_RE.match(pid)
            if not pm:
                errors.append(f"{name}:{lineno}: {pid!r} is not "
                              f"<chunk>#<kind><n>")
                continue
            base, kind, _ = pm.groups()

            if pid in seen:
                errors.append(f"{name}:{lineno}: point {pid} already defined in "
                              f"{seen[pid]}")
            seen[pid] = f"{name}:{lineno}"

            if kind not in KINDS:
                errors.append(f"{name}:{lineno}: {pid} has unknown kind "
                              f"{kind!r}")
            if chunk != base:
                errors.append(f"{name}:{lineno}: {pid} says chunk {chunk!r}, "
                              f"but its id is built on {base!r}")
            if base not in chunks:
                errors.append(f"{name}:{lineno}: {pid} points at chunk {base}, "
                              f"which does not exist")
            elif not chunks[base][1]:
                errors.append(f"{name}:{lineno}: {pid} points at {base}, which "
                              f"is retrieve: never and must not be indexed")

            if not what:
                errors.append(f"{name}:{lineno}: {pid} has no description")
            elif len(what.split()) > MAX_WORDS:
                warnings.append(f"{name}:{lineno}: {pid} description is "
                                f"{len(what.split())} words, target {MAX_WORDS}")
            if not alias:
                no_alias += 1

            per_chunk[base] = per_chunk.get(base, 0) + 1
            per_kind[kind] = per_kind.get(kind, 0) + 1
        files[name] = n
        if n == 0:
            errors.append(f"{name}: no point rows parsed — check the table format")

    # A retrievable chunk with no points is invisible to a point-level query.
    for cid, (fname, retrievable) in sorted(chunks.items()):
        if retrievable and cid not in per_chunk:
            warnings.append(f"{cid} ({fname}) has no points — a point-level "
                            f"query can never reach it")

    print(f"{len(seen)} points across {len(files)} files, "
          f"covering {len(per_chunk)}/{sum(1 for c in chunks.values() if c[1])} "
          f"retrievable chunks")
    for name, n in sorted(files.items()):
        print(f"  {n:>4}  {name}")
    print("kinds: " + "  ".join(f"{k}={v}" for k, v in sorted(per_kind.items())))
    print(f"rows with no `also called`: {no_alias}")

    thin = sorted((n, c) for c, n in per_chunk.items())[:5]
    print("thinnest coverage: " + ", ".join(f"{c} ({n})" for n, c in thin))

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
