path = "embed.py"
src = open(path).read()
if "_unit" in src:
    print("Patch pehle se laga hua hai.")
else:
    marker = "class VectorIndex:"
    if marker not in src:
        print("embed.py ka format alag hai. Patch nahi lagaya.")
    else:
        head = src[:src.index(marker)]
        tail = '''import operator


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
'''
        open(path, "w").write(head + tail)
        print("Patch lag gaya.")
