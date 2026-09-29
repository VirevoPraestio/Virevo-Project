"""Tojo v2 — chunk lint.

Checked against the whole library at once, because the failures that matter are
cross-file: an id that two files both claim, a `needs` pointing at a section that
was split or retired, a chunk the index card forgot.

Run against a directory holding the v2 reference files and index cards:

    python3 lint_chunks.py --refs <dir> --index <dir>

Exits non-zero on any error. Warnings do not fail the build.
"""

import argparse
import glob
import os
import re
import sys

CHUNK_RE = re.compile(r"<!--chunk\s*\n(.*?)\n-->", re.S)
# Inline maintainer spans: kept in the file, stripped before assembly.
MSPAN_RE = re.compile(r"<!--m-->.*?<!--/m-->", re.S)
REQUIRED = ("id", "title", "summary", "keys", "needs", "see", "tokens")
OPTIONAL = ("retrieve",)
PREFIXES = ("bed", "dis", "opd", "common", "play")

MIN_TOKENS, MAX_TOKENS = 400, 2000
MAX_NEEDS = 2      # hard dependencies only; more means the split was wrong
SUMMARY_MAX = 200

# A runtime file must not reason about its own recency or completeness.
BANNED = [
    (re.compile(r"\b20\d\d-\d\d-\d\d\b"), "a date"),
    (re.compile(r"\bstill open\b", re.I), "a status note"),
    (re.compile(r"\bTODO\b", re.I), "a TODO"),
    (re.compile(r"\bturn \d+\b", re.I), "a hard turn number"),
    (re.compile(r"\bworth watching\b", re.I), "a hedge"),
    (re.compile(r"\bnot yet settled\b", re.I), "a hedge"),
]


def parse(path):
    text = open(path).read()
    out = []
    for m in CHUNK_RE.finditer(text):
        fields, order = {}, []
        for line in m.group(1).split("\n"):
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip()
            fields[k] = v.strip()
            order.append(k)
        fields["_span"] = m.span()
        fields["_order"] = order
        out.append(fields)
    return text, out


def body_of(text, chunks, i):
    start = chunks[i]["_span"][1]
    end = chunks[i + 1]["_span"][0] if i + 1 < len(chunks) else len(text)
    return text[start:end]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", required=True)
    ap.add_argument("--index", required=True)
    a = ap.parse_args()

    errors, warnings = [], []
    all_ids, needs_edges, see_edges, never = {}, [], [], set()
    totals = {}

    for path in sorted(glob.glob(os.path.join(a.refs, "*.md"))):
        name = os.path.basename(path)
        text, chunks = parse(path)
        if not chunks:
            errors.append(f"{name}: no chunk front-matter at all")
            continue
        total = 0
        for i, c in enumerate(chunks):
            cid = c.get("id", f"<missing id, chunk {i}>")

            for f in REQUIRED:
                if f not in c or not c[f]:
                    errors.append(f"{name} {cid}: missing required field `{f}`")
            for f in c["_order"]:
                if f not in REQUIRED + OPTIONAL:
                    errors.append(f"{name} {cid}: unknown field `{f}`")

            if "id" in c:
                if c["id"] in all_ids:
                    errors.append(f"{name} {cid}: id already claimed by "
                                  f"{all_ids[c['id']]}")
                all_ids[c["id"]] = name
                if c["id"].split(".")[0] not in PREFIXES:
                    errors.append(f"{name} {cid}: prefix not in {PREFIXES}")

            if c.get("retrieve"):
                if c["retrieve"] != "never":
                    errors.append(f"{name} {cid}: retrieve must be `never`, "
                                  f"got {c['retrieve']!r}")
                never.add(c.get("id"))

            s = c.get("summary", "")
            if len(s) > SUMMARY_MAX:
                errors.append(f"{name} {cid}: summary {len(s)} chars, "
                              f"max {SUMMARY_MAX}")
            if s and s.rstrip().endswith(":"):
                warnings.append(f"{name} {cid}: summary reads as a label, "
                                f"not a statement")

            keys = [k.strip() for k in c.get("keys", "").split(",") if k.strip()]
            if not 4 <= len(keys) <= 10:
                warnings.append(f"{name} {cid}: {len(keys)} keys, expected 4-10")

            try:
                tok = int(c.get("tokens", "0"))
                total += tok
                if tok > MAX_TOKENS:
                    warnings.append(f"{name} {cid}: {tok} tokens, over the "
                                    f"{MAX_TOKENS} target")
                if tok < MIN_TOKENS:
                    warnings.append(f"{name} {cid}: {tok} tokens, under the "
                                    f"{MIN_TOKENS} target")
            except ValueError:
                errors.append(f"{name} {cid}: tokens is not a number")

            n = c.get("needs", "").strip()
            if n and n != "none":
                deps = [d.strip() for d in n.split(",") if d.strip()]
                if len(deps) > MAX_NEEDS:
                    errors.append(f"{name} {cid}: {len(deps)} needs, max "
                                  f"{MAX_NEEDS} — the extras are `see` entries, "
                                  f"or the chunk should not have been split")
                for dep in deps:
                    needs_edges.append((name, c.get("id"), dep))
            sv = c.get("see", "").strip()
            if sv and sv != "none":
                for dep in [d.strip() for d in sv.split(",") if d.strip()]:
                    see_edges.append((name, c.get("id"), dep))

            # A retrievable chunk must not carry maintainer content.
            if not c.get("retrieve"):
                body = MSPAN_RE.sub("", body_of(text, chunks, i))
                for pat, what in BANNED:
                    m = pat.search(body)
                    if m:
                        errors.append(f"{name} {cid}: body contains {what} "
                                      f"({m.group(0)!r}) in a retrievable chunk")
        totals[name] = (len(chunks), total)

    for name, src, dep in needs_edges + see_edges:
        if dep not in all_ids:
            errors.append(f"{name} {src}: needs `{dep}`, which does not exist")
        elif dep in never:
            errors.append(f"{name} {src}: needs `{dep}`, which is "
                          f"retrieve: never")
        elif dep == src:
            errors.append(f"{name} {src}: needs itself")

    for path in sorted(glob.glob(os.path.join(a.index, "*.card.md"))):
        card = open(path).read()
        prefix = os.path.basename(path).split(".")[0]
        if prefix == "GROUP-CATALOGUE":
            continue
        listed = set(re.findall(rf"\|\s*({prefix}\.[\w.\-]+)\s*\|", card))
        owned = {i for i in all_ids if i.split(".")[0] == prefix}
        for missing in sorted(owned - listed):
            errors.append(f"{prefix}.card.md: chunk {missing} is not listed")
        for extra in sorted(listed - owned):
            errors.append(f"{prefix}.card.md: lists {extra}, which does not exist")
        for nid in sorted(owned & never & listed):
            row = [ln for ln in card.split("\n") if nid in ln]
            if row and not re.search(r"never", row[0], re.I):
                warnings.append(f"{prefix}.card.md: {nid} is retrieve: never but "
                                f"its row does not say so")

    print(f"{len(all_ids)} chunks across {len(totals)} files")
    for name, (n, tok) in sorted(totals.items()):
        print(f"  {n:>3} chunks  {tok:>6} tokens  {name}")
    retr = sum(1 for i in all_ids if i not in never)
    print(f"retrievable: {retr}   never: {len(never)}   "
          f"needs (hard): {len(needs_edges)}   see (soft): {len(see_edges)}")

    # The check the first pass did not have: what a one-hop fetch actually costs.
    tok = {}
    for path in sorted(glob.glob(os.path.join(a.refs, "*.md"))):
        for c in parse(path)[1]:
            try:
                tok[c.get("id")] = int(c.get("tokens", 0))
            except ValueError:
                tok[c.get("id")] = 0
    hard = {}
    for _, src, dep in needs_edges:
        hard.setdefault(src, set()).add(dep)
    worst = []
    for cid in all_ids:
        if cid in never:
            continue
        pulled = {cid} | hard.get(cid, set())     # one hop, never to fixpoint
        worst.append((sum(tok.get(i, 0) for i in pulled), len(pulled), cid))
    worst.sort(reverse=True)
    lib = sum(t for i, t in tok.items() if i not in never)
    print("worst-case one-hop pull:")
    for t, n, cid in worst[:3]:
        print(f"  {cid:<22} {n} chunks, {t} tokens ({100 * t / lib:.0f}% of library)")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
