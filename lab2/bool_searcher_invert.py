from base.serializer import BaseSerializer
from base.bool_ops import WordOp, AndOp, OrOp, NotOp, ZeroOp

class BoolSearcherInvert():
    def __init__(self, serializer:BaseSerializer ,invert_index_file: str, doc_ids: set):
        self.serializer = serializer
        self.invert_index_file = invert_index_file
        self.doc_ids = doc_ids
        self.load()

    def load(self):
        print(self.invert_index_file)
        self.invert_index = self.serializer.deserealize(self.invert_index_file)

    def search(self, word: WordOp):
        if word.__class__.__name__ == ZeroOp.__name__:
            return self.invert_index.get(word.word, [])

        if word.__class__.__name__ == AndOp.__name__:
            ind1 = self.search(word.word1)
            ind2 = self.search(word.word2)
            return list(set(ind1) & set(ind2))

        if word.__class__.__name__ == OrOp.__name__:
            ind1 = self.search(word.word1)
            ind2 = self.search(word.word2)
            return list(set(ind1) | set(ind2))

        if word.__class__.__name__ == NotOp.__name__:
            ind1 = self.search(word.word1)
            return list(self.doc_ids.difference(set(ind1)))