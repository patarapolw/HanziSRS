import sqlite3
import jieba

from HanziSRS.dir import user_path


class User:
    def __init__(self):
        self.db = sqlite3.connect(user_path('user.db'))

    def sentence_to_vocab(self):
        cursor = self.db.execute('SELECT * FROM user_sentence')
        for row in cursor:
            for word in jieba.cut_for_search(row[1]):
                yield word

    def load_user_vocab(self):
        cursor = self.db.execute('SELECT * FROM user_vocab')
        for row in cursor:
            yield row[1]
            yield row[2]

    def load_user_sentence(self):
        cursor = self.db.execute('SELECT * FROM user_sentence')
        for row in cursor:
            yield row[1]


if __name__ == '__main__':
    User().load_user_sentence()
