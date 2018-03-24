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
        else:
            is_at_least_2_char = False
        self._lookup_params = list(iter_lookup_params())

    @pyqtProperty(str)
    def get_lookup_params(self):
        return json.dumps(self._lookup_params)


class QTsv(QObject):
    filename = NotImplemented  # type: str
    chinese_column = NotImplemented  # type: str
    index_column = NotImplemented  # type: int
    encoding = 'utf8'

    def __init__(self):
        super().__init__()
        self.entries = dict()
        with open(database_path(self.filename), encoding=self.encoding) as f:
            keys = f.readline().strip().split('\t')
            for row in f:
                values = row.strip().split('\t')
                self.entries[values[self.index_column]] = dict(zip(keys, values))

        self._lookup = []
        self._lookup_params = []

    @pyqtProperty(str)
    def get_dump(self):
        return json.dumps(self.entries)

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        def iter_lookup():
            if vocab:
                for entry in self.entries.values():
                    if vocab == entry[self.chinese_column]:
                        yield entry
        self._lookup = list(iter_lookup())

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
                            if item[k] == v:
                                yield entry

        param_dict = json.loads(params)
        if 'settings' in param_dict:
            param_dict.pop('settings')
        self._lookup_params = list(iter_lookup_params())

    @pyqtProperty(str)
    def get_lookup_params(self):
        return json.dumps(self._lookup_params)


class SpoonFed(QTsv):
    def __init__(self):
        self.filename = 'SpoonFed.tsv'
        self.chinese_column = 'Chinese'
        self.index_column = -1
        super().__init__()

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        def iter_lookup():
            if vocab:
                for entry in self.entries.values():
                    if re.search(vocab.replace('…', '.*'), entry['Chinese']):
                        yield entry
        self._lookup = list(iter_lookup())


class HanziVariant(QTsv):
    def __init__(self):
        self.filename = 'hanzi_variant.tsv'
        self.chinese_column = 'Character'
        self.index_column = 1
        super().__init__()

        entries_update = dict()
        for key, entry in self.entries.items():
            if 'Variant' not in entry.keys():
                self.entries[key]['Variant'] = ''
            for char in entry['Variant']:
                if char not in self.entries.keys():
                    entries_update[char] = entry

        self.entries.update(entries_update)

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        def iter_lookup():
            if vocab:
                for entry in self.entries.values():
                    if vocab in (entry[self.chinese_column]+entry['Variant']):
                        yield entry
        self._lookup = list(iter_lookup())


class VocabCategory(QObject):
    def __init__(self):
        super().__init__()
        self.entries = dict()
        vocab = ''
        reading = ''
        english = ''
        category = NotImplemented  # type: str

        with open(database_path('vocab_category.txt')) as f:
            for row in f:
                match_obj = re.match(r'([^\t]*)\t([^\t]*)\t([^\t]*)[\t\n]', row)
                if not match_obj:
                    category = row.strip().lower()
                    if not category:
                        continue
                else:
                    vocab, reading, english = match_obj.groups()

                if vocab:
                    if vocab not in self.entries.keys():
                        self.entries[vocab] = {
                            'vocab': vocab,
                            'reading': reading,
                            'english': english,
                            'categories': [category]
                        }
                    else:
                        if category not in self.entries[vocab]['categories']:
                            self.entries[vocab]['categories'].append(category)

        self._lookup = dict()
        self._lookup_category = []
        self._categories = dict()
        self._category = ''
        self._do_categories()

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        self._lookup = self.entries[vocab]

    @pyqtProperty(str)
    def get_lookup(self):
        return json.dumps(self._lookup)

    @pyqtSlot(str)
    def do_lookup_category(self, category):
        def iter_lookup():
            for entry in self.entries.values():
                if category in entry['categories']:
                    yield entry
        self._lookup_category = list(iter_lookup())

    @pyqtProperty(str)
    def get_lookup_category(self):
        return json.dumps(self._lookup_category)

    def _do_categories(self):
        for entry in self.entries.values():
            for category in entry['categories']:
                self._categories[category] = self._categories.setdefault(category, 0) + 1

    @pyqtProperty(str)
    def get_categories(self):
        return json.dumps(self._categories)
