from itertools import chain
import re

from analyze.user_db import User
from analyze.tag import HskVocab, Category, HanziLevelProject
from analyze.lookup import Cedict, SpoonFed


class Analysis:
    def __init__(self):
        self.user = User()
        self.ref = {
            'hsk': HskVocab(),
            'category': Category(),
            'hlp': HanziLevelProject(),
            'dict': Cedict(),
            'sentence': SpoonFed()
        }

        self.vocabs = []
        used_vocab = []
        # for vocab in self.user.sentence_to_vocab():
        for vocab in self.user.load_user_vocab():
        # for vocab in set(chain(self.user.sentence_to_vocab(), self.user.load_user_vocab())):
            lookup = self.ref['dict'].get(vocab)
            simplified = lookup.get('simplified', '')
            vocab = simplified if simplified else vocab

            if vocab not in used_vocab:
                used_vocab.append(vocab)
                if re.search(r'[\u2E80-\u2FD5\u3400-\u4DBF\u4E00-\u9FCC]', vocab):
                    self.vocabs.append((vocab, self.to_note(vocab)))
                else:
                    print('Skipped', vocab)

        self.sentences = []
        for sentence in self.user.load_user_sentence():
            self.sentences.append((sentence, self.to_tags(sentence, 'sentence')))

        hanzi_list = list(set(re.findall(r'[\u2E80-\u2FD5\u3400-\u4DBF\u4E00-\u9FCC]',
                                         ''.join([entry for entry, content in chain(self.vocabs, self.sentences)]))))
        self.hanzi = [(hanzi, self.to_tags(hanzi, 'hanzi')) for hanzi in hanzi_list]

        self.tags = {
            'hanzi': [],
            'vocab': [],
            'sentence': []
        }
        for _, note in self.vocabs:
            self.tags['vocab'].extend(note['tags'])
        for _, tags in self.sentences:
            self.tags['sentence'].extend(tags)
        for _, tags in self.hanzi:
            self.tags['hanzi'].extend(tags)

    def to_note(self, vocab):
        hanzi_level = ''
        hanzi_level_and_category = self.ref['hlp'].vocab_to_level_and_category(vocab)
        if hanzi_level_and_category:
            hanzi_level = re.findall(r'\d+', hanzi_level_and_category[0])[0]
        lookup = self.ref['dict'].get(vocab)
        simp = lookup.get('Simplified', '')
        trad = lookup.get('traditional', '')

        return {
            'fields': {
                'Simplified': simp if simp else vocab,
                'Traditional': trad if trad != simp else '',
                'Pinyin': lookup.get('reading', ''),
                'English': lookup.get('english', ''),
                'Hanzi level': hanzi_level,
                'Note': self.ref['sentence'].formatted_lookup(vocab)
            },
            'tags': self.to_tags(vocab, 'vocab'),
        }

    def to_tags(self, entry, type_of_entry):
        tags = []
        level = self.ref['hsk'].what_level(entry)
        if level:
            tags.append(level)
        for category in self.ref['category'].what_category(entry, type_of_entry):
            tags.append(category)
        hanzi_level_and_category = self.ref['hlp'].vocab_to_level_and_category(entry)
        if hanzi_level_and_category:
            tags.extend(hanzi_level_and_category)

        return tags


if __name__ == '__main__':
    a = Analysis()
    print(a.vocabs)
    print(a.sentences)
