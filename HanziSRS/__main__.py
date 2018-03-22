import sys
import sqlite3

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from HanziSRS.db import HskVocab, SpoonFed
from HanziSRS.user import User, UserVocab, UserHanzi
from HanziSRS.utils import Utils
from HanziSRS.dir import qml_path, user_path


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    hsk_vocab = HskVocab()
    context.setContextProperty('pyHskVocab', hsk_vocab)
    spoonfed = SpoonFed()
    context.setContextProperty('pySentence', spoonfed)
    utils = Utils()
    context.setContextProperty('py', utils)

    user = User()
    context.setContextProperty('pyUser', user)

    user_db = sqlite3.connect(user_path('user.db'))
    user_vocab = UserVocab(user_db)
    user_hanzi = UserHanzi(user_db)
    context.setContextProperty('pyUserVocab', user_vocab)
    context.setContextProperty('pyUserHanzi', user_hanzi)

    engine.load(qml_path("main.qml"))
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
