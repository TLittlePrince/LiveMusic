import sys
import json
from ui_file.coldDownUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication

with open('setting.json', 'r') as f_obj:
    setting = json.load(f_obj)


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.doubleSpinBox.setValue(setting['time'])
        self.ui.doubleSpinBox.valueChanged.connect(self.save_time)

    @pyqtSlot(float)
    def save_time(self, value):
        setting['time'] = value
        with open('setting.json', 'w') as f:
            json.dump(setting, f)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.close()


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    # win.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
    win.show()
    sys.exit(app.exec_())

