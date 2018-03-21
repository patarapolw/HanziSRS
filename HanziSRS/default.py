from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty

from HanziSRS.dir import user_path


class Default(QObject):
    def __init__(self, database=user_path('default.db')):
        super().__init__()
