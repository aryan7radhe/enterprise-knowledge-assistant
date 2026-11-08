def rrf(rank_lists, k=60):
    """Do (ya zyada) librarians ki ranking ko milao.
    Jo doc dono ki list me upar ho, uska number sabse bada."""
    scores = {}
    for lst in rank_lists:
        for rank, (doc_id, _) in enumerate(lst):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: -x[1])
