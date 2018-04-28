import subprocess
import sys
if sys.platform != 'darwin':
    from google_speech import Speech

from PyQt5.QtCore import QObject, pyqtSlot


class Utils(QObject):
    @pyqtSlot(str)
    def speak(self, word):
        if sys.platform == 'darwin':
            subprocess.Popen(['say', '-v', 'ting-ting', word])
        else:
            Speech(word, 'zh-CN')
