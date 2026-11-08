import time
from loader import build_chunks
from embed import VectorIndex

t0 = time.time()
chunks = build_chunks("data/corpus", size=200, overlap=40, min_words=40)
texts = {c["id"]: c["text"] for c in chunks}
print(f"{len(chunks)} chunks ke embeddings bana rahe hain (beech me Ctrl+C dabao toh bhi theek hai)...")
VectorIndex(texts)
print(f"Ho gaya: {time.time() - t0:.0f} second")
