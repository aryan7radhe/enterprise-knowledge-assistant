import hashlib
import json
import math
import os
import sys
import urllib.request

EMBED_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "nomic-embed-text"
CACHE_FILE = "embed_cache.json"
BATCH = 32

_cache = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, encoding="utf-8") as f:
        _cache = json.load(f)


def _key(text):
    return hashlib.md5((EMBED_MODEL + text).encode("utf-8")).hexdigest()


def _call_ollama(texts):
    body = {"model": EMBED_MODEL, "input": texts}
    req = urllib.request.Request(
        EMBED_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode("utf-8"))["embeddings"]


def _save():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(_cache, f)


def embed(texts):
    """Text ki list do, numbers ki list (address) wapas lo.
    Naye texts 32-32 ke batch me bhejta hai aur har batch ke baad disk par save karta hai,
    toh beech me ruk jaye tab bhi kaam bachta hai."""
    missing = list(dict.fromkeys(t for t in texts if _key(t) not in _cache))
    n_batches = (len(missing) + BATCH - 1) // BATCH
    for b, start in enumerate(range(0, len(missing), BATCH)):
        batch = missing[start:start + BATCH]
        for t, v in zip(batch, _call_ollama(batch)):
            _cache[_key(t)] = v
        if b % 10 == 9 or b == n_batches - 1:      # har 10 batch par aur aakhir me save
            _save()
        if len(missing) > BATCH:
            print(f"  embeddings: {min(start + BATCH, len(missing))}/{len(missing)}", file=sys.stderr, flush=True)
    return [_cache[_key(t)] for t in texts]


def cosine(a, b):
    """Do addresses kitne paas hain? 1 = bilkul paas, 0 = koi rishta nahi."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


import operator


def _unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v] if n else v


class VectorIndex:
    """Matlab samajhne wala librarian. Vectors ko pehle hi 'unit' bana leta hai,
    taaki har sawal par sirf ek multiply-add chale (tez)."""

    def __init__(self, docs):
        self.ids = list(docs)
        raw = embed(["search_document: " + docs[i] for i in self.ids])
        self.vecs = [_unit(v) for v in raw]

    def search(self, query, k=3):
        q = _unit(embed(["search_query: " + query])[0])
        scored = [(i, sum(map(operator.mul, q, v))) for i, v in zip(self.ids, self.vecs)]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]
