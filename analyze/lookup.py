import re

from HanziSRS.dir import database_path


class Cedict:
    def __init__(self):
        super().__init__()
        self.dictionary = dict()
        with open(database_path('cedict_ts.u8'), encoding='utf8') as f:
            for row in f.readlines():
                result = re.fullmatch(r'(\w+) (\w+) \[(.+)\] /(.+)/\n', row)
                if result is not None:
                    trad, simp, pinyin, eng = result.groups()
                    self.dictionary.setdefault(simp, [])
                    self.dictionary.setdefault(trad, [])
                    self.dictionary[simp].append({
                        'traditional': trad,
                        'simplified': simp,
                        'reading': pinyin,
                        'english': eng
                    })
                    if trad != simp:
                        self.dictionary[trad].append(self.dictionary[simp][-1])

    def get(self, vocab):
        return self.dictionary.get(vocab, [dict()])[0]


class SpoonFed:
    def __init__(self):
        self.entries = []
        with open(database_path('SpoonFed.tsv')) as f:
            next(f)
            for row in f:
                contents = row.split('\t')
                self.entries.append({
                    'Chinese': contents[2],
                    'English': contents[0]
                })

    def formatted_lookup(self, vocab):
        result = ''
        for item in self.iter_lookup(vocab):
            result += item['Chinese'] + '<br />'
            result += item['English'] + '<br />'
        return result

    def iter_lookup(self, vocab):
        if vocab:
            for entry in self.entries:
                if re.search(vocab.replace('…', '.*'), entry['Chinese']):
                    yield entry
