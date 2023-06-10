
from typing import List
from base.base import BaseProcesser, BaseParser, BaseSerializer, Document
from collections import defaultdict, OrderedDict
import os

class PhraseProcessor(BaseProcesser):

    def __init__(self, parser: BaseParser, serializer: BaseSerializer):
        super().__init__(parser, serializer)
        self._phrase_index = defaultdict(list)

    def _process_word(self, document: Document, word: str):
        phrase = self.prev_word + ' ' + word

        if not self._phrase_index[phrase] or document.id != self._phrase_index[phrase][-1]:
            self._phrase_index[phrase].append(document.id)
        self.prev_word = word
        
    def _after_collection_action(self, files_pathes: List[str]):
        self._serializer.serialize(self._phrase_index, '../res/phrase.json')
        print('res_size_mb: ', os.stat('../res/phrase.json').st_size / (1024 * 1024))

    def _before_file_action(self, doc: Document):
        self.prev_word = ''