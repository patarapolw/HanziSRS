import json
import re

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty

from HanziSRS.dir import database_path


class HskVocab(QObject):
    def __init__(self):
        super().__init__()
        self.entries = dict()
        with open(database_path('hsk_vocab.tsv')) as f:
            keys = f.readline().strip().split('\t')
            for row in f:
                item = row.strip().split('\t')
                self.entries.setdefault(item[0], []).append(dict(zip(keys, item)))
                # if item[1] and item[1] != item[0]:
                #     self.entries.setdefault(item[1], []).append(dict(zip(keys, item)))

        self._lookup = []
        self._lookup_params = []

    @pyqtSlot(str)
    def do_lookup(self, word):
        self._lookup = self.entries.get(word, dict())

    @pyqtProperty(str)
    def get_lookup(self):
        return json.dumps(self._lookup)

    @pyqtSlot(str)
    def do_lookup_params(self, params):
        def iter_lookup_params():
            for k, v in param_dict.items():
                n = ''.join(re.findall(r'\d+', k))
                if not n:
                    n = '1'
                for i in range(1, int(n)+1):
                    k = re.sub(r'\d+', str(i), k)
                    for entry in self.entries.values():
                        for item in entry:
                            if is_at_least_2_char:
                                if len(item['Simplified']) <= 2:
                                    continue
                            if item[k] == v:
                                yield entry

        param_dict = json.loads(params)
        if 'settings' in param_dict:
            is_at_least_2_char = param_dict.pop('settings')['at_least_2_char']
        self._lookup_params = list(iter_lookup_params())

    @pyqtProperty(str)
    def get_lookup_params(self):
        return json.dumps(self._lookup_params)


class SpoonFed(QObject):
    def __init__(self):
        super().__init__()
        self.entries = dict()
        with open(database_path('SpoonFed.tsv'), encoding='utf8') as f:
            keys = f.readline().strip().split('\t')
            for row in f:
                values = row.strip().split('\t')
                self.entries[values[-1]] = dict(zip(keys, values))

        self._lookup = []

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        def iter_lookup():
            if vocab:
                for entry in self.entries.values():
                    if re.search(re.sub(r'…', r'.*', vocab), entry['Chinese']):
                        yield entry
        self._lookup = list(iter_lookup())

    @pyqtProperty(str)
    def get_lookup(self):
        return json.dumps(self._lookup)
