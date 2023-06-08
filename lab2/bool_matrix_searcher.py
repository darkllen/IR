from base.serializer import BaseSerializer
from lab2.bool_ops import WordOp, AndOp, OrOp, NotOp, ZeroOp

class BoolSearcherMatrix():
    def __init__(self, serializer:BaseSerializer , matrix_file: str, words_file: str):
        self.serializer = serializer
        self.matrix_file = matrix_file
        self.words_file = words_file
        self.load()

    def load(self):
        self.matrix = self.serializer.deserealize(self.matrix_file)
        self.words = self.serializer.deserealize(self.words_file)

    def search(self, word: WordOp):
        l = self.search_helper(word)
        l = [i for i, s in enumerate(l) if s==1]
        return l

    def search_helper(self, word: WordOp):
        if word.__class__.__name__ == ZeroOp.__name__:
            ind = self.words.index(word.word)
            if ind == -1:
                return []
            return self.matrix[ind]

        if word.__class__.__name__ == AndOp.__name__:
            ind1 = self.search_helper(word.word1)
            ind2 = self.search_helper(word.word2)
            return ind1 and ind2

        if word.__class__.__name__ == OrOp.__name__:
            ind1 = self.search_helper(word.word1)
            ind2 = self.search_helper(word.word2)
            return ind1 or ind2

        if word.__class__.__name__ == NotOp.__name__:
            ind1 = self.search_helper(word.word1)
            return list(map(lambda val: 1 - val, ind1))