import re
from loader import build_chunks
from bm25 import BM25
from embed import VectorIndex
from hybrid import rrf
from llm import ask_llm

MODE = "vector"        # "bm25", "vector" ya "hybrid"
K = 3
MIN_BM25 = 1.5         # BM25 ke liye "pata nahi" ki seema
MIN_COSINE = 0.55      # vector ke liye "pata nahi" ki seema (apne data se chuni)

chunks = build_chunks("docs")
by_id = {c["id"]: c for c in chunks}
texts = {c["id"]: c["text"] for c in chunks}
bm = BM25(texts)
vec = VectorIndex(texts)

NOT_FOUND = "Mujhe documents me iska jawab nahi mila."


def retrieve(question):
    """Sawal ke liye sabse achhe tukde dhoondho."""
    if MODE == "bm25":
        found = [(i, s) for i, s in bm.search(question, k=K) if s >= MIN_BM25]
    elif MODE == "vector":
        found = [(i, s) for i, s in vec.search(question, k=K) if s >= MIN_COSINE]
    else:  # hybrid
        top = vec.search(question, k=1)
        if not top or top[0][1] < MIN_COSINE:
            return []
        found = rrf([bm.search(question, k=5), vec.search(question, k=5)])[:K]
    return [by_id[i] for i, _ in found]


def make_prompt(question, contexts):
    """LLM ko sirf diye gaye tukdon se jawab dene ka hukm do."""
    context_text = "\n\n".join(f"[{i + 1}] {c['text']}" for i, c in enumerate(contexts))
    return (
        "You are a company knowledge assistant. Answer the question using ONLY the "
        "context below. Keep the answer short (1-3 sentences). After the answer, cite "
        "the numbers of the context pieces you used, like [1]. If the context does not "
        "contain the answer, reply exactly: I don't know.\n\n"
        f"CONTEXT:\n{context_text}\n\nQUESTION: {question}\n\nANSWER:"
    )


def ask(question):
    contexts = retrieve(question)
    if not contexts:
        return NOT_FOUND, []
    answer = ask_llm(make_prompt(question, contexts))
    if "don't know" in answer.lower().replace("\u2019", "'"):
        return NOT_FOUND, []
    # sirf wahi sources dikhao jinka number jawab me likha hai, jaise [1]
    cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", answer) if 1 <= int(n) <= len(contexts)})
    if not cited:
        cited = list(range(1, len(contexts) + 1))
    sources = [f'[{n}] {contexts[n - 1]["source"]}' for n in cited]
    return answer, sources


if __name__ == "__main__":
    print(f"{len(chunks)} chunks load hue. Mode: {MODE}. Sawal poochho ('exit' likhkar band karo).")
    while True:
        q = input("\nSawal: ").strip()
        if q.lower() == "exit":
            break
        answer, sources = ask(q)
        print("\nJawab:", answer)
        for s in sources:
            print("  Source:", s)
