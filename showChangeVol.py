import sys
import json
import utils
import atexit
from ui_file.changeVolUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication


with open('setting.json', 'r') as f_obj:
    setting = json.load(f_obj)


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setting = setting
        atexit.register(self.e)
        self.ui.horizontalSlider.setValue(self.setting['vol'])
        self.ui.horizontalSlider.valueChanged.connect(self.save_vol)

    @pyqtSlot(int)
    def save_vol(self, value):
        self.setting['vol'] = value
        utils.change_vol(value)
        self.e()

    @pyqtSlot()
    def e(self):
        with open('setting.json', 'w') as f:
            json.dump(self.setting, f)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    # win.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
    win.show()
    sys.exit(app.exec_())
