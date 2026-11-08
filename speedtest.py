import time
from loader import build_chunks
from embed import embed

chunks = build_chunks("data/corpus", size=200, overlap=40, min_words=40)
N = min(64, len(chunks))
texts = ["search_document: " + c["text"] for c in chunks[:N]]
t0 = time.time()
embed(texts)
dt = time.time() - t0
rate = N / dt
print(f"{N} chunks ke embeddings: {dt:.1f} second  ->  {rate:.1f} chunks/second")
print(f"Kul {len(chunks)} chunks ke liye andaza: {len(chunks) / rate / 60:.1f} minute")
print("(Yeh chunks cache me save ho gaye, kaam bekaar nahi gaya.)")
