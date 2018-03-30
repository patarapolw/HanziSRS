import re

from HanziSRS.dir import database_path


class HskVocab:
    def __init__(self):
        self.entries = dict()
        with open(database_path('hsk_vocab.tsv')) as f:
            for row in f:
                contents = row.split('\t')
                level = contents[-3][-1]
                if level.isdigit():
                    self.entries.setdefault(contents[-3], []).append(contents[0])

    def what_level(self, vocab):
        for level, vocab_list in self.entries.items():
            if vocab in vocab_list:
                return level

        return None


class Category:
    def __init__(self):
        self.entries = dict()
        with open(database_path('vocab_category.txt')) as f:
            category = None
            vocab_list = None
            for row in f:
                contents = row.split('\t')
                if len(contents) == 1:
                    if category and vocab_list:
                        self.entries[category] = vocab_list
                    category = contents[0].strip()
                    vocab_list = []
                else:
                    vocab_list.append(contents[0])

    def what_category(self, vocab):
        for category, vocab_list in self.entries.items():
            if vocab in vocab_list:
                yield category


class HanziLevelProject:
    def __init__(self):
        self.entries = []
        with open(database_path('hanzi_level.txt')) as f:
            category = None
            for row in f:
                if row[0].isdigit():
                    category = row.strip()
                else:
                    self.entries.append((row.strip(), category))

    def hanzi_to_level_and_category(self, hanzi):
        for i, hanzi_list in enumerate(self.entries):
            if hanzi in hanzi_list[0]:
                return 'HLP_Level_{}'.format(i+1), hanzi_list[1]
        return None

    def vocab_to_level_and_category(self, vocab):
        def search_iter():
            for hanzi in vocab:
                result = self.hanzi_to_level_and_category(hanzi)
                if result:
                    yield result
        x = list(search_iter())
        if x:
            return max(x, key=lambda entry: int(re.findall(r'\d+', entry[0])[0]))
        else:
            return None


if __name__ == '__main__':
    hlp = HanziLevelProject()
    print(hlp.vocab_to_level_and_category('你好'))
