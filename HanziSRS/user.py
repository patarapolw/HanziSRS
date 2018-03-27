import os
import json
from time import time

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty

from HanziSRS.dir import user_path
from HanziSRS.srs import next_review_timestamp, correct_next_srs


class User(QObject):
    def __init__(self, database=user_path('user.json')):
        super().__init__()
        self.database = database
        if os.path.exists(self.database):
            with open(self.database) as f:
                self._user = json.load(f)
        else:
            self._user = dict()

        self._cred = self._user.setdefault('cred', {
                'user_name': '',
                'vocab_level': 1,
                'hanzi_level': 1,
                'reading_level': 1,
        })
        self._settings = self._user.setdefault('settings', {
            'at_least_2_char': True,
            "srs_interval": {
                "learning": ["1h", "4h", "8h"],
                "review": ["1d", "3d", "1w", "4w", "4mo"]
            }
        })
        self._state = self._user.setdefault('state', {
            'sentence': 1
        })

    def save(self):
        with open(self.database, 'w') as f:
            json.dump(self._user, f, indent=2)

    @pyqtProperty(str)
    def get_user(self):
        return json.dumps(self._user)

    @pyqtSlot(str)
    def set_user(self, user):
        self._user = json.loads(user)
        self.save()

    @pyqtProperty(str)
    def get_cred(self):
        return json.dumps(self._cred)

    @pyqtSlot(str)
    def set_cred(self, cred):
        self._cred = json.loads(cred)
        self._user['cred'] = self._cred
        self.save()

    @pyqtProperty(str)
    def get_settings(self):
        return json.dumps(self._settings)

    @pyqtSlot(str)
    def set_settings(self, settings):
        self._settings = json.loads(settings)
        self._user['settings'] = self._settings
        self.save()


class AbstractDatabase(QObject):
    table = NotImplemented      # type: str
    headers = NotImplemented    # type: list

    def __init__(self, database):
        """

        :type database: SQLite Object
        """
        super().__init__()
        # self.table = 'user_vocab'
        # self.headers = ['ass_sounds', 'ass_meanings' 'notes']
        # self.db = sqlite3.connect(user_path('user.db'))
        self.db = database

        query_string = '''CREATE TABLE IF NOT EXISTS {} (
            id INT PRIMARY KEY NOT NULL,''' \
            + ('{} TEXT,'*len(self.headers))[:-1]\
            + ');'
        self.db.execute(query_string.format(self.table, *self.headers))
        self.db.commit()

        self._lookup = []

    def __iter__(self):
        return self.db.execute('SELECT * FROM {}'.format(self.table))

    @pyqtSlot(list)
    def do_submit(self, headers):
        if len(headers) != len(self.headers):
            raise IndexError('List must be of length {}'.format(len(self.headers)))
        self.do_delete(headers[0])

        srs = int(headers[self.headers.index("srs")])
        srs_type = headers[self.headers.index("is_learning_or_review")]
        srs, srs_type = correct_next_srs(srs, srs_type)
        headers[self.headers.index("next_review")] = next_review_timestamp(srs, srs_type)

        query_string = 'INSERT INTO {} (id,' + ('{},'*len(self.headers))[:-1] \
                       + ') VALUES (?,' + ('?,'*len(self.headers))[:-1] + ');'
        self.db.execute(query_string.format(self.table, *self.headers),
                        (int(time() * 1000), *headers))
        self.db.commit()

    @pyqtSlot(str)
    def do_lookup(self, key):
        key_header, *lookup_headers = self.headers
        query_string = 'SELECT ' + ('{},'*(len(self.headers)-1))[:-1] + ' FROM {} WHERE {}=?;'
        formatter = lookup_headers + [self.table] + [key_header]
        cursor = self.db.execute(query_string.format(*formatter), (key,))
        self._lookup = cursor.fetchone()

    @pyqtProperty(list)
    def get_lookup(self):
        if self._lookup:
            return list(self._lookup)
        else:
            return []

    @pyqtSlot(str)
    def do_delete(self, key):
        cursor = self.db.execute('''SELECT id FROM {} WHERE {}=?;'''.format(self.table, self.headers[0])
                                 , (key,))
        id_tuple = cursor.fetchone()
        if id_tuple is not None:
            self.db.execute('''DELETE FROM {} WHERE id=?;'''.format(self.table), id_tuple)
            self.db.commit()

    @pyqtProperty(list)
    def get_dump(self):
        return [list(item) for item in self]


class UserVocab(AbstractDatabase):
    def __init__(self, database):
        self.table = 'user_vocab'
        self.headers = ['vocab_simp', 'vocab_trad', 'ass_sounds', 'ass_meanings', 'notes',
                        'is_learning_or_review', 'srs', 'next_review']  # new: 0, learning: 1, review: 2
        super().__init__(database)


class UserHanzi(AbstractDatabase):
    def __init__(self, database):
        self.table = 'user_hanzi'
        self.headers = ['hanzi', 'rel_hanzi', 'rel_vocab', 'notes',
                        'is_learning_or_review', 'srs', 'next_review']
        super().__init__(database)


class UserSentence(AbstractDatabase):
    def __init__(self, database):
        self.table = 'user_sentence'
        self.headers = ['sentence', 'rel_hanzi', 'rel_vocab', 'notes',
                        'is_learning_or_review', 'srs', 'next_review']
        super().__init__(database)
