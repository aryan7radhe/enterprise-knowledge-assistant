import sys
from collections import Counter
from loader import build_chunks

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "data/corpus"
chunks = build_chunks(FOLDER, size=200, overlap=40, min_words=40)
per_file = Counter(c["source"] for c in chunks)
print(f"Kul chunks: {len(chunks)}")
print("Sabse zyada chunks wali 15 files:")
for path, n in per_file.most_common(15):
    print(f"  {n:4d}  {path}")
top = sum(n for _, n in per_file.most_common(15))
print(f"\nIn 15 files ke chunks: {top} ({100 * top / len(chunks):.0f}% of total)")
