
from typing import List
from base.base import BaseProcesser, BaseParser, BaseSerializer, Document
from collections import defaultdict, OrderedDict
import os

class CoordinateProcessor(BaseProcesser):

    def __init__(self, parser: BaseParser, serializer: BaseSerializer):
        super().__init__(parser, serializer)
        self._coordinate_index = defaultdict(lambda: defaultdict(list))

    def _process_word(self, document: Document, word: str):
        self._coordinate_index[word][document.id].append(self.pos)
        self.pos+=1
        
    def _after_collection_action(self, files_pathes: List[str]):
        self._serializer.serialize(self._coordinate_index, '../res/coordinate.json')
        print('res_size_mb: ', os.stat('../res/coordinate.json').st_size / (1024 * 1024))

    def _before_file_action(self, doc: Document):
        self.pos = 0