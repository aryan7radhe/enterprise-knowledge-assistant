import math
import re
from collections import Counter

STOP = set("a an the is are was be to of in on for and or do does did i my me we our "
           "you your it its how what when where who why which at by with from as that "
           "this there any".split())


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    words = [w for w in words if w not in STOP]
    # plural hatao: "requests" -> "request"
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in words]


class BM25:
    """Smart librarian: shabd gino, aur RARE shabdon ko zyada number do."""

    def __init__(self, docs, k1=1.5, b=0.75):
        self.ids = list(docs)
        self.k1, self.b = k1, b
        self.tf = {i: Counter(tokenize(docs[i])) for i in self.ids}
        self.len = {i: sum(self.tf[i].values()) for i in self.ids}
        self.avgdl = sum(self.len.values()) / len(self.ids)
        n = len(self.ids)
        df = Counter()
        for c in self.tf.values():
            df.update(c.keys())
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def score(self, qtokens, doc_id):
        s = 0.0
        tf, dl = self.tf[doc_id], self.len[doc_id]
        for w in qtokens:
            if w in tf:
                f = tf[w]
                s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
        return s

    def search(self, query, k=3):
        q = tokenize(query)
        scored = [(i, self.score(q, i)) for i in self.ids]
        scored = [x for x in scored if x[1] > 0]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]
