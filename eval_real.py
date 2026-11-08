import math
import time
from loader import build_chunks
from bm25 import BM25
from embed import VectorIndex
from hybrid import rrf

K_CHUNKS = 30
t0 = time.time()
chunks = build_chunks("data/corpus", size=200, overlap=40, min_words=40)
by_id = {c["id"]: c for c in chunks}
texts = {c["id"]: c["text"] for c in chunks}
bm = BM25(texts)
vec = VectorIndex(texts)

with open("testset.tsv", encoding="utf-8") as f:
    rows = [line.rstrip("\n").split("\t") for line in f if "\t" in line]
in_corpus = {c["source"] for c in chunks}
tests = [(q, s) for q, s in rows if s in in_corpus]
print(f"{len(chunks)} chunks, {len(tests)} sawal ({len(rows) - len(tests)} sawal ki file corpus me nahi mili, chhode)")


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), min(1, c + h)


def file_ranks(ranking):
    files = []
    for cid, _ in ranking:
        f = by_id[cid]["source"]
        if f not in files:
            files.append(f)
    return files


methods = {"BM25 (shabd)": [], "Vector (matlab)": [], "Hybrid (RRF)": []}
for q, gold in tests:
    b = bm.search(q, k=K_CHUNKS)
    v = vec.search(q, k=K_CHUNKS)
    h = rrf([b, v])[:K_CHUNKS]
    for name, ranking in zip(methods, (b, v, h)):
        files = file_ranks(ranking)
        methods[name].append(files.index(gold) + 1 if gold in files else None)

n = len(tests)
print(f"\n{'Tareeka':<18}{'R@1':>6}{'R@3':>6}{'R@5':>6}{'R@10':>6}{'MRR':>7}   R@3 ka 95% daayra")
for name, ranks in methods.items():
    def r(k):
        return sum(1 for x in ranks if x is not None and x <= k)
    mrr = sum(1 / x for x in ranks if x is not None and x <= 10) / n
    lo, hi = wilson(r(3), n)
    print(f"{name:<18}{100 * r(1) / n:5.0f}%{100 * r(3) / n:5.0f}%{100 * r(5) / n:5.0f}%{100 * r(10) / n:5.0f}%{mrr:7.2f}   {100 * lo:.0f}%-{100 * hi:.0f}%")

all_fail = [tests[i] for i in range(n) if all(methods[m][i] is None or methods[m][i] > 3 for m in methods)]
print(f"\nTeeno tareeke top-3 me fail: {len(all_fail)} sawal")
for q, s in all_fail[:10]:
    print(f"  - {q}\n      (chahiye: {s})")
print(f"\nTime: {time.time() - t0:.0f} second")
