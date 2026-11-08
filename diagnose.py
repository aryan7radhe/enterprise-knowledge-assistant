from loader import build_chunks
from bm25 import BM25
from embed import VectorIndex
from hybrid import rrf

K_CHUNKS = 30
chunks = build_chunks("data/corpus", size=200, overlap=40, min_words=40)
by_id = {c["id"]: c for c in chunks}
texts = {c["id"]: c["text"] for c in chunks}
bm = BM25(texts)
vec = VectorIndex(texts)

with open("testset.tsv", encoding="utf-8") as f:
    rows = [line.rstrip("\n").split("\t") for line in f if "\t" in line]
in_corpus = {c["source"] for c in chunks}
tests = [(q, s) for q, s in rows if s in in_corpus]


def file_ranks(ranking):
    files = []
    for cid, _ in ranking:
        f = by_id[cid]["source"]
        if f not in files:
            files.append(f)
    return files


failed = []
for q, gold in tests:
    b = bm.search(q, k=K_CHUNKS)
    v = vec.search(q, k=K_CHUNKS)
    h = rrf([b, v])[:K_CHUNKS]
    fb, fv, fh = file_ranks(b), file_ranks(v), file_ranks(h)
    if all(gold not in fl[:3] for fl in (fb, fv, fh)):
        failed.append((q, gold, fh))

near = 0
print(f"Teeno tareeke top-3 me fail: {len(failed)} sawal\n")
for n, (q, gold, fh) in enumerate(failed, 1):
    pos = fh.index(gold) + 1 if gold in fh else None
    near += 1 if pos and pos <= 10 else 0
    print(f"[{n}] SAWAL : {q}")
    print(f"    GOLD  : {gold}")
    print(f"    Hybrid me gold ki jagah: {pos if pos else '30 chunks ke andar nahi'}")
    print("    Hybrid ke top-3 files:")
    for f in fh[:3]:
        print(f"       - {f}")
    print()
print(f"In {len(failed)} me se {near} me gold file top-10 ke andar thi (yaani 'kareeb-kareeb' miss).")
