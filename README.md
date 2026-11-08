# Enterprise Knowledge Assistant (RAG)

A retrieval-augmented question-answering assistant built from scratch in Python (standard library only) over the public GitLab handbook. Answers are generated locally with Ollama and cite their sources.

## What is inside
- `loader.py` - Markdown cleaning (front matter, shortcodes, images, links) and overlapping chunking
- `bm25.py` - keyword search (BM25) written from scratch
- `embed.py` - embedding search with Ollama (nomic-embed-text), batched and cached on disk
- `hybrid.py` - Reciprocal Rank Fusion of keyword and embedding rankings
- `llm.py`, `app.py` - local LLM (llama3.2) answers with citations and an "I don't know" guard
- `eval_real.py`, `diagnose.py` - retrieval evaluation (recall@k, MRR, Wilson 95% intervals) and failure analysis
- `make_testset.py` - LLM-drafted evaluation questions, filtered by hand

## Retrieval results
65 reviewed questions over 3,645 chunks. Each question has one known source file.

| Method | Recall@3 | Recall@10 | MRR |
|---|---|---|---|
| BM25 | 69% | 80% | 0.62 |
| Embeddings | 77% | 82% | 0.67 |
| Hybrid (RRF) | 74% | 88% | 0.68 |

The 95% confidence intervals overlap, so these differences are a trend, not a proven win.

## Limitations
- Only one gold file per question, so scores are a lower bound (several files can answer the same question).
- Questions were drafted by an LLM and filtered by hand; they can share words with the source text, which may favour BM25.
- Small test set (65 questions). Vector search is pure Python. No reranker and no access control yet.
- The "I don't know" score threshold was calibrated on a small sample and is not yet validated at this scale.

## Run it
1. Install [Ollama](https://ollama.com), then `ollama pull llama3.2` and `ollama pull nomic-embed-text`
2. `bash setup_data.sh` (downloads the handbook and builds `data/corpus`)
3. `python3 build_index.py` (one-time embeddings; resumable, takes a while)
4. `python3 eval_real.py` (compares BM25, embeddings and hybrid)
5. `python3 app.py` (interactive chat; the `build_chunks(...)` line near the top chooses the sample `docs/` folder or `data/corpus`)

No `pip install` is needed.

## Data
The handbook is not included in this repository. `setup_data.sh` downloads it from https://gitlab.com/gitlab-com/content-sites/handbook. Please check its license and keep attribution.

## Roadmap
FastAPI backend and chat UI, per-department access control at retrieval time, a reranker, Docker.
