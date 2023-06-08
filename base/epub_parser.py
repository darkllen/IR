
from typing import Iterable
from base.base import BaseParser
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import nltk
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup



class EpubParser(BaseParser):
        
    def _get_words(self, file_path: str) -> Iterable[str]:
        book = epub.read_epub(file_path)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        for item in items:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = [para.get_text() for para in soup.find_all('p')]
            for p in text:
                for word in (a for a in nltk.word_tokenize(p) if a.isascii() and a.isalpha()):
                    yield word
        
    