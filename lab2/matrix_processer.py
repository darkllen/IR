from typing import List
from base.base import BaseProcesser, BaseParser, BaseSerializer, Document
from collections import defaultdict, OrderedDict
import os


class MatrixProcessor(BaseProcesser):
    def __init__(self, parser: BaseParser, serializer: BaseSerializer):
        super().__init__(parser, serializer)
        self._matrix = defaultdict(set)

    def _process_word(self, document: Document, word: str):
        if not self._matrix[word] or document.id not in self._matrix[word]:
            self._matrix[word].add(document.id)
    
    def _after_collection_action(self, files_pathes: List[str]):
        si = len(files_pathes)
        f = lambda x: [1 if s in x else 0 for s in range(si)]

        s = {k: f(v) for k, v in self._matrix.items()}
        sorted_keys = sorted(self._matrix.keys())
        s = [s[k] for k in sorted_keys]

        self._serializer.serialize(s, "../res/matrix.json")
        self._serializer.serialize(sorted_keys, "../res/words_sorted.json")
        print("res_size_mb_1: ", os.stat("../res/words_sorted.json").st_size / (1024 * 1024))
        print("res_size_mb_2: ", os.stat("../res/matrix.json").st_size / (1024 * 1024))