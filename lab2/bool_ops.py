class WordOp:

    @staticmethod
    def and_op(word1: "WordOp", word2:"WordOp"):
        return AndOp(word1, word2)

    @staticmethod
    def or_op(word1: "WordOp", word2:"WordOp"):
        return OrOp(word1, word2)

    @staticmethod
    def not_op(word: "WordOp"):
        return NotOp(word)

    @staticmethod
    def zero_op(word: str):
        return ZeroOp(word)

class AndOp(WordOp):
    
    def __init__(self, word1: "WordOp", word2:"WordOp") -> None:
        self.word1 = word1
        self.word2 = word2

class OrOp(WordOp):
    def __init__(self, word1: "WordOp", word2:"WordOp") -> None:
        self.word1 = word1
        self.word2 = word2

class NotOp(WordOp):
    def __init__(self, word1) -> None:
        self.word1 = word1

class ZeroOp(WordOp):
    def __init__(self, word1) -> None:
        self.word = word1