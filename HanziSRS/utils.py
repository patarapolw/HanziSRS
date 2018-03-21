import subprocess
import sys
from google_speech import Speech

from PyQt5.QtCore import QObject, pyqtSlot


class Utils(QObject):
    @pyqtSlot(str)
    def speak(self, word):
        if sys.platform == 'darwin':
            subprocess.call(['say', '-v', 'ting-ting', word])
        else:
            Speech(word, 'zh-CN')
