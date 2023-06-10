import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from typing import Generator, Any
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

import re
from enum import Enum
from abc import ABC, abstractmethod
from typing import Iterable, List, Any, Generic, TypeVar
from pydantic import BaseModel
import os

class Document(BaseModel):
    id: int
    name: str

T = TypeVar("T")


class BaseSerializer(ABC, Generic[T]):
    @abstractmethod
    def serialize(self, obj: T, file_path: str) -> None:
        pass

    @abstractmethod
    def deserealize(self, file_path: str) -> T:
        pass


class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, word: str) -> str:
        ...


class BaseParser(ABC):
    def __init__(self, normalizer: BaseNormalizer) -> None:
        self._normalizer = normalizer

    def get_iterator(self, file_path: str) -> Iterable[str]:
        for word in self._get_words(file_path):
            yield self._normalizer.normalize(word)

    @abstractmethod
    def _get_words(self, file_path: str) -> Iterable[str]:
        ...


class BaseProcesser(ABC):
    def __init__(self, parser: BaseParser, serializer: BaseSerializer):
        self._parser = parser
        self._serializer = serializer

    def process(self, files_pathes: List[str]) -> None:
        self._before_collection_action(files_pathes)
        for id, file_path in enumerate(files_pathes):
            try:
                doc = Document(id=id, name=file_path)
                self._before_file_action(doc)
                for word in self._parser.get_iterator(file_path):
                    self._process_word(doc, word)

                self._after_file_action(doc)
            except Exception as e:
                print('Error', e)
        self._after_collection_action(files_pathes)

    def _process_word(self, doc: Document, word: str):
        ...

    def _before_file_action(self, doc: Document):
        ...

    def _after_collection_action(self, files_pathes: List[str]):
        ...

    def _after_file_action(self, doc: Document):
        print(doc)

    def _before_collection_action(self, files_pathes: List[str]):
        init_size = 0
        for filename in files_pathes:
            init_size += os.stat(filename).st_size
        print("books_num: ", len(files_pathes))
        print("size_mb: ", init_size / (1024 * 1024))

# def get_content_iterator(
#     file_path: str, encoding: str = "utf-8", normalize: Normalize = Normalize.NO
# ) -> Generator[str, Any, None]:
#     fb2_book = ET.iterparse(
#         open(file_path, "r", encoding=encoding), events=["start", "end"]
#     )
#     stemmer = PorterStemmer()
#     lemmer = WordNetLemmatizer()

#     parse_flag = False
#     for event, elem in fb2_book:
#         el: Element = elem
#         if el.tag.rpartition("}")[-1] == "body" and event == "start":
#             parse_flag = True

#         if el.tag.rpartition("}")[-1] == "body" and event == "end":
#             parse_flag = False

#         if el.tag.rpartition("}")[-1] == "p" and event == "start" and parse_flag:
#             for text in el.itertext():
#                 for word in (
#                     a.lower() for a in nltk.word_tokenize(text) if a.isalpha()
#                 ):
#                     if normalize == Normalize.STEMMER:
#                         word = stemmer.stem(word)
#                     elif normalize == Normalize.LEMMER:
#                         word = lemmer.lemmatize(word)

#                     yield word
