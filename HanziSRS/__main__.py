import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from HanziSRS.db import HskVocab, SpoonFed
from HanziSRS.user import UserCred
from HanziSRS.utils import Utils
from HanziSRS.dir import qml_path


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load(qml_path("main.qml"))
    engine.quit.connect(app.quit)
    context = engine.rootContext()

    hsk_vocab = HskVocab()
    context.setContextProperty('pyHskVocab', hsk_vocab)
    spoonfed = SpoonFed()
    context.setContextProperty('pySentence', spoonfed)
    utils = Utils()
    context.setContextProperty('py', utils)

    user_cred = UserCred()
    context.setContextProperty('pyUserCred', user_cred)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
