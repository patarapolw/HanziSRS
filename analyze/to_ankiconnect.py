from itertools import chain
from AnkiTools import AnkiConnect as ac
import re

from analyze.user_db import User
from analyze.tag import HskVocab, Category, HanziLevelProject
from analyze.lookup import Cedict, SpoonFed


class AnkiConnect():
    def __init__(self):
        self.user = User()
        self.hsk = HskVocab()
        self.cat = Category()
        self.hlp = HanziLevelProject()
        self.cedict = Cedict()
        self.sentence = SpoonFed()

    def do_vocab(self):
        to_unsuspend = []
        to_add = []
        all_vocabs = set(chain(self.user.sentence_to_vocab(), self.user.load_user_vocab()))
        try:
            for i, vocab in enumerate(all_vocabs):
                print("Submitting entry: {} of {}".format(i+1, len(all_vocabs)))
                if re.search(r'[\u2E80-\u2FD5\u3400-\u4DBF\u4E00-\u9FCC]', vocab):
                    if self.hsk.what_level(vocab):
                        print("To unsuspend", vocab)
                        to_unsuspend.extend(
                            [int(x) for x in
                             ac.POST('findCards', params={'query': "(Simplified:{0} OR Traditional:{0})"
                                     .format(vocab)})['result']])
                    else:
                        print("Queuing:", vocab)
                        to_add.append(self.to_note(vocab))
                else:
                    print("Skipped:", vocab)
        except KeyboardInterrupt:
            pass

        print('Unsuspend count:', len(to_unsuspend))
        print('Unsuspending:', to_unsuspend)
        print(ac.POST('unsuspend', params={'cards': to_unsuspend}))

        print('Attempted add note count:', len(to_add))
        print('Checking if can add notes.')
        can_add = []
        for i, canAddNote in enumerate(ac.POST('canAddNotes', params={'notes': to_add})['result']):
            if canAddNote:
                can_add.append(to_add[i])

        print('Addable note count:', len(can_add))
        print('Adding notes.')
        print(ac.POST('addNotes', params={'notes': can_add}))

        print('Changing decks:')
        self.change_decks()

    def to_note(self, vocab):
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
        return {
            'deckName': deck_name,
            'modelName': "Chinese Custom Vocab",
            'fields': {
                'Simplified': lookup.get('Simplified', '') if lookup.get('Simplified', '') else vocab,
                'Traditional': lookup.get('traditional', ''),
                'Pinyin': lookup.get('reading', ''),
                'English': lookup.get('english', ''),
                'Hanzi level': hanzi_level,
                'Note': self.sentence.formatted_lookup(vocab)
            },
            'tags': tags,
        }

    def change_decks(self):
        cards = [
            'Simplified',
            'Traditional',
            'English'
        ]
        for card, deck in cards:
            to_change = ac.POST('findCards', params={'query': "added:1 card:{}".format(card)})['result']
            print(ac.POST('changeDeck', params={'cards': to_change,
                                                'deck': 'Chinese::Vocab Extra::{}'.format(card)}))


if __name__ == '__main__':
    AnkiConnect().do_vocab()
