from base.base import BaseNormalizer
import nltk


class LemmerNormalizer(BaseNormalizer):
    def __init__(self) -> None:
        nltk.download('wordnet')
        self._lemmer = nltk.WordNetLemmatizer()

    def normalize(self, word: str) -> str:
        return self._lemmer.lemmatize(word.lower())
