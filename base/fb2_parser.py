
from typing import Iterable
from base.base import BaseParser
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import nltk


class Fb2Parser(BaseParser):
        
    def _get_words(self, file_path: str) -> Iterable[str]:
        fb2_book = ET.iterparse(
            open(file_path, "r", encoding='utf-8'), events=["start", "end"]
        )
        parse_flag = False
        for event, elem in fb2_book:
            el: Element = elem
            if el.tag.rpartition("}")[-1] == "body" and event == "start":
                parse_flag = True

            if el.tag.rpartition("}")[-1] == "body" and event == "end":
                parse_flag = False

            if el.tag.rpartition("}")[-1] == "p" and event == "start" and parse_flag:
                for text in el.itertext():
                    for word in (a for a in nltk.word_tokenize(text) if a.isalpha()):
                        yield word
