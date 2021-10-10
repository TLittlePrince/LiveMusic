import sys
from ui_file.aboutUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QCoreApplication


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(427, 275)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    win.show()
    sys.exit(app.exec_())
