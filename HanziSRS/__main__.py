import sys
import sqlite3

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from HanziSRS.db import HskVocab, SpoonFed, HanziVariant, VocabCategory, HanziLevel, Cedict
from HanziSRS.user import User, UserVocab, UserHanzi, UserSentence
from HanziSRS.utils import Utils
from HanziSRS.dir import qml_path, user_path


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    hsk_vocab = HskVocab()
    spoonfed = SpoonFed()
    hanzi_variant = HanziVariant()
    vocab_category = VocabCategory()
    hanzi_level = HanziLevel()
    cedict = Cedict()
    context.setContextProperty('pyHskVocab', hsk_vocab)
    context.setContextProperty('pySentence', spoonfed)
    context.setContextProperty('pyHanziVariant', hanzi_variant)
    context.setContextProperty('pyVocabCategory', vocab_category)
    context.setContextProperty('pyHanziLevel', hanzi_level)
    context.setContextProperty('pyCedict', cedict)

    utils = Utils()
    context.setContextProperty('py', utils)

    user = User()
    context.setContextProperty('pyUser', user)

    user_db = sqlite3.connect(user_path('user.db'))
    user_vocab = UserVocab(user_db)
    user_hanzi = UserHanzi(user_db)
    user_sentence = UserSentence(user_db)
    context.setContextProperty('pyUserVocab', user_vocab)
    context.setContextProperty('pyUserHanzi', user_hanzi)
    context.setContextProperty('pyUserSentence', user_sentence)

    engine.load(qml_path("main.qml"))
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
