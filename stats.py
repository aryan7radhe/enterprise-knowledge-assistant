import sys
from collections import Counter
from loader import build_chunks

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "data/corpus"
chunks = build_chunks(FOLDER, size=200, overlap=40, min_words=40)
if not chunks:
    print(f"{FOLDER} me koi chunk nahi bana. Folder ka path ya copy wala step check karo.")
    sys.exit(1)
files = {c["source"] for c in chunks}
print(f"Kam se kam 40 shabd wali files : {len(files)}")
print(f"Kul chunks                      : {len(chunks)}")
print(f"Ek chunk me average shabd       : {sum(len(c['text'].split()) for c in chunks) / max(1, len(chunks)):.0f}")
print()
print("Department ke hisaab se chunks:")
for dept, n in Counter(c["dept"] for c in chunks).most_common():
    print(f"  {n:5d}  {dept}")
print()
mid = chunks[len(chunks) // 2]
print("Beech ka ek namuna chunk:")
print("  id   :", mid["id"])
print("  title:", mid["title"])
print("  text :", mid["text"][:400].replace("\n", " / "), "...")
