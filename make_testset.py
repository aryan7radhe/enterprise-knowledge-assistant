import json
import os
import random
from loader import build_chunks
from llm import ask_llm

N_FILES = 80
OUT = "testset_draft.jsonl"
BANNED = ("passage", "the text", "document", "handbook", "above", "following", "according to")

PROMPT = (
    "Below is a passage from a company handbook. Write ONE question that a new employee "
    "might ask, which this passage answers clearly.\n"
    "Rules:\n"
    "- Use plain everyday words. Do NOT copy long phrases from the passage.\n"
    "- Do NOT mention 'the passage', 'the text', 'the document' or 'the handbook'.\n"
    "- The question must make sense on its own, without seeing the passage.\n"
    "- Output ONLY the question, nothing else.\n\n"
    "PASSAGE:\n{text}\n\nQUESTION:"
)


def clean_question(raw):
    q = raw.strip().split("\n")[0].strip().strip('"').strip()
    for prefix in ("Question:", "Q:"):
        if q.startswith(prefix):
            q = q[len(prefix):].strip()
    return q


def is_good(q):
    n = len(q.split())
    if not q.endswith("?") or n < 5 or n > 30:
        return False
    low = q.lower()
    return not any(b in low for b in BANNED)


chunks = build_chunks("data/corpus", size=200, overlap=40, min_words=40)
by_file = {}
for c in chunks:
    by_file.setdefault(c["source"], []).append(c)

files = sorted(by_file)
random.Random(42).shuffle(files)
files = files[:N_FILES]

done = set()
if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        for line in f:
            done.add(json.loads(line)["source"])

with open(OUT, "a", encoding="utf-8") as out:
    for i, source in enumerate(files, 1):
        if source in done:
            continue
        pieces = by_file[source]
        long_enough = [c for c in pieces if len(c["text"].split()) >= 120] or pieces
        chunk = random.Random(f"42-{source}").choice(long_enough)
        raw = ask_llm(PROMPT.format(text=chunk["text"]))
        q = clean_question(raw)
        ok = (not raw.startswith("[LLM error")) and is_good(q)
        print(f"[{i}/{len(files)}] {source}\n    -> {q if ok else '(chhod diya)'}", flush=True)
        out.write(json.dumps({"source": source, "dept": chunk["dept"], "question": q if ok else None}) + "\n")
        out.flush()

good = []
with open(OUT, encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r["question"]:
            good.append(r)
with open("testset.tsv", "w", encoding="utf-8") as f:
    for r in good:
        f.write(f"{r['question']}\t{r['source']}\n")
print(f"\n{len(good)} achhe sawal testset.tsv me save hue.")
