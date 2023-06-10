
from typing import List
from base.base import BaseProcesser, BaseParser, BaseSerializer, Document
from collections import defaultdict, OrderedDict
import os

class InvertProcessor(BaseProcesser):

    def __init__(self, parser: BaseParser, serializer: BaseSerializer):
        super().__init__(parser, serializer)
        self._invert_index = defaultdict(list)

    def _process_word(self, document: Document, word: str):
        if not self._invert_index[word] or document.id != self._invert_index[word][-1]:
            self._invert_index[word].append(document.id)
        
    def _after_collection_action(self, files_pathes: List[str]):
        self._serializer.serialize(self._invert_index, '../res/invert.json')
        print('res_size_mb: ', os.stat('../res/invert.json').st_size / (1024 * 1024))