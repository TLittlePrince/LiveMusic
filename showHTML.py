import sys
from ui_file.htmlUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QCoreApplication


with open('html/read.html', 'r', encoding='utf-8') as f_obj:
    html = f_obj.read()


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.textBrowser.setHtml(html)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    # win.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
    win.show()
    sys.exit(app.exec_())
