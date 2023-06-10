from base.serializer import BaseSerializer
from base.bool_ops import WordOp, AndOp, OrOp, NotOp, ZeroOp

class CoordinateSearcher():
    def __init__(self, serializer:BaseSerializer ,coordinate_index_file: str, doc_ids: set):
        self.serializer = serializer
        self.coordinate_index_file = coordinate_index_file
        self.doc_ids = doc_ids
        self.load()

    def load(self):
        print(self.coordinate_index_file)
        self.coordinate_index = self.serializer.deserealize(self.coordinate_index_file)

    def _min_dist(self, l1, l2, k):
        i = j = 0
        minimum = float('inf')
        m = len(l1)
        z = len(l2)
        while i < m and j < z:
            diff = l1[i] - l2[j]
            minimum = min(minimum, abs(diff))
            if minimum <= k:
                return True
            if diff < 0:
                i += 1
            elif diff > 0:
                j += 1
            else:
                break
        return False

    def search(self, word: WordOp, k:int=1):
        l = self.search_helper(word, k)
        return l

    def search_helper(self, word: WordOp, k: int = 1):
        if word.__class__.__name__ == ZeroOp.__name__:
            return self.coordinate_index.get(word.word, {})

        if word.__class__.__name__ == AndOp.__name__:

            ind1 = self.search_helper(word.word1, k)
            ind2 = self.search_helper(word.word2, k)

            l = []
            same_keys = [k for k in ind1 if k in ind2]
            for ke in same_keys:
                pos1 = ind1[ke]
                pos2 = ind2[ke]
                if self._min_dist(pos1, pos2, k):
                    l.append(ke)
            return l

        if word.__class__.__name__ == OrOp.__name__:
            ind1 = self.search_helper(word.word1)
            ind2 = self.search_helper(word.word2)
            return list(set(ind1) | set(ind2))

        if word.__class__.__name__ == NotOp.__name__:
            ind1 = self.search_helper(word.word1)
            return list(self.doc_ids.difference(set(ind1)))