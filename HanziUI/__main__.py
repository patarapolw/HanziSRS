import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory

from analyze import Analysis

from HanziUI.dir import ui_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_path('main.ui'), self)

        self.user = Analysis()

        self.hanzi_level.setText('1')
        self.tag_browser.setText(self.print_tags())
        self.tag_browser.anchorClicked.connect(self.add_tag)
        self.show()

    def print_tags(self):
        html = ''
        tags = ['random']
        tags.extend(sorted(set(self.user.tags)))
        for tag in tags:
            html += "<a href='{0}'>{0}</a>, &emsp; ".format(tag)

        return html

    def add_tag(self, link):
        self.tag_input.setText(link.toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    win = MainWindow()
    sys.exit(app.exec_())
