from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty

from HanziSRS.dir import user_path


class UserCred(QObject):
    def __init__(self, database=user_path('user_home.db')):
        super().__init__()
        self._vocab_level = 1
        self._hanzi_level = 1
        self._reading_level = 1

    @pyqtProperty(int)
    def get_vocab_level(self):
        return self._vocab_level

    @pyqtSlot(int)
    def set_vocab_level(self, level):
        self._vocab_level = level

    @pyqtProperty(int)
    def get_hanzi_level(self):
        return self._hanzi_level

    @pyqtSlot(int)
    def set_hanzi_level(self, level):
        self._hanzi_level = level

    @pyqtProperty(int)
    def get_reading_level(self):
        return self._reading_level

    @pyqtSlot(int)
    def set_reading_level(self, level):
        self._reading_level = level
