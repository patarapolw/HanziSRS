from itertools import chain
import re

from analyze.user_db import User
from analyze.tag import HskVocab, Category, HanziLevelProject
from analyze.lookup import Cedict, SpoonFed
from export.anki.log import Logger


class Vocab:
    def __init__(self):
        self.user = User()
        self.hsk = HskVocab()
        self.cat = Category()
        self.hlp = HanziLevelProject()
        self.cedict = Cedict()
        self.sentence = SpoonFed()

        self.to_unsuspend = list()
        self.to_add = list()
        all_vocabs = set(chain(self.user.sentence_to_vocab(), self.user.load_user_vocab()))
        for i, vocab in enumerate(all_vocabs):
            if re.search(r'[\u2E80-\u2FD5\u3400-\u4DBF\u4E00-\u9FCC]', vocab):
                if self.hsk.what_level(vocab):
                    self.to_unsuspend.append(vocab)
                else:
                    self.to_add.append(vocab)
            else:
                print("Skipped:", vocab)

        with Logger('anki.log.yaml') as log:
            log_dict = log.load()
            self.to_add = [item for item in self.to_add if item not in log_dict.get('to_add', [])]
            self.to_unsuspend = [item for item in self.to_unsuspend
                                 if item not in log_dict.get('to_unsuspend', [])]
            log.save(**{
                'to_add': self.to_add,
                'to_unsuspend': self.to_unsuspend
            })

    def to_tsv(self, filename):
        '''
        modelName: "Chinese Custom Vocab"
        '''
        fields_names = ['Simplified', 'Traditional', 'Pinyin', 'English', 'Hanzi level', 'Note', 'tags']

        with open(filename, 'w') as f:
            for vocab in self.to_add:
                tags = []
                deck_name = 'Default'
                hanzi_level = ''
                level = self.hsk.what_level(vocab)
                if level:
                    tags.append(level)
                for category in self.cat.what_category(vocab):
                    tags.append(category)
                hanzi_level_and_category = self.hlp.vocab_to_level_and_category(vocab)
                if hanzi_level_and_category:
                    tags.extend(hanzi_level_and_category)
                    hanzi_level = re.findall(r'\d+', hanzi_level_and_category[0])[0]
                lookup = self.cedict.get(vocab)
                simplified = lookup.get('Simplified', '')
                traditional = lookup.get('traditional', '')
                fields = [
                    simplified if simplified else vocab,
                    traditional if simplified != traditional else '',
                    lookup.get('reading', ''),
                    lookup.get('english', ''),
                    hanzi_level,
                    self.sentence.formatted_lookup(vocab),
                    ' '.join(tags)
                ]
                assert len(fields_names) == len(fields), "Please recheck if the number and the order of the fields"

                f.write('\t'.join(fields) + '\n')

    def unsuspend_to_query(self):
        for i in range(0, len(self.to_unsuspend), 50):
            try:
                print(' OR '.join(['Simplified:{0} OR Traditional:{0}'.format(item)
                                   for item in self.to_unsuspend[i: i+50]]))
            except IndexError:
                print(' OR '.join(['Simplified:{0} OR Traditional:{0}'.format(item)
                                   for item in self.to_unsuspend[i:]]))


class Sentence:
    def __init__(self):
        self.user = User()
        self.logger = Logger('anki.log.yaml')

        self.to_unsuspend = []
        for sentence in self.user.load_user_sentence():
            self.to_unsuspend.append(sentence)

    def unsuspend_to_query(self):
        for item in sum(self.logger.load_var('to_unsuspend'), []):
            self.to_unsuspend.remove(item)
        self.logger.save_var(to_unsuspend=self.to_unsuspend)

        for i in range(0, len(self.to_unsuspend), 50):
            try:
                print(' OR '.join(['Hanzi:{0}'.format(item)
                                   for item in self.to_unsuspend[i: i+50]]))
            except IndexError:
                print(' OR '.join(['Hanzi:{0}'.format(item)
                                   for item in self.to_unsuspend[i:]]))


if __name__ == '__main__':
    a = Vocab()
    a.unsuspend_to_query()
    a.to_tsv('custom_vocab.tsv')
