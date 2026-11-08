from loader import build_chunks
from bm25 import BM25
from embed import VectorIndex
from hybrid import rrf

# eval.py se sawal ki list utha lo (dobara type karne se bachne ke liye)
_src = open("eval.py").read()
_start = _src.index("TESTS = [")
_end = _src.index("\n]\n", _start) + 3
exec(_src[_start:_end])

K = 3
chunks = build_chunks("docs")
by_id = {c["id"]: c for c in chunks}
texts = {c["id"]: c["text"] for c in chunks}
bm = BM25(texts)
vec = VectorIndex(texts)


def bm25_ids(q):
    return [i for i, s in bm.search(q, k=K) if s >= 1.5]


def vector_ids(q):
    return [i for i, s in vec.search(q, k=K)]


def hybrid_ids(q):
    return [i for i, _ in rrf([bm.search(q, k=5), vec.search(q, k=5)])[:K]]


def sources(ids):
    return [by_id[i]["source"] for i in ids]


answerable = [t for t in TESTS if t[1] is not None]
unanswerable = [t for t in TESTS if t[1] is None]

print(f"{'Tareeka':<22}{'Sahi file mili (recall@3)'}")
for name, fn in [("BM25 (shabd)", bm25_ids), ("Vector (matlab)", vector_ids), ("Hybrid (dono)", hybrid_ids)]:
    hits, misses = 0, []
    for q, expected in answerable:
        if expected in sources(fn(q)):
            hits += 1
        else:
            misses.append(q)
    print(f"{name:<22}{hits}/{len(answerable)} = {100 * hits / len(answerable):.0f}%")
    for q in misses:
        print(f"      MISS: {q}")

# "pata nahi" ki seema (threshold) tay karne ke liye
ans_scores = [vec.search(q, k=1)[0][1] for q, _ in answerable]
un_scores = [vec.search(q, k=1)[0][1] for q, _ in unanswerable]
print()
print("Vector top-score (cosine):")
print(f"  jinka jawab docs me hai   -> sabse chhota {min(ans_scores):.3f}, average {sum(ans_scores) / len(ans_scores):.3f}")
print(f"  jinka jawab docs me nahi  -> sabse bada   {max(un_scores):.3f}")
