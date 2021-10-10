import os
import sys
import json
from ui_file.changeRoomUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QCoreApplication

os.environ['Path'] = os.environ['Path'] + ';' + os.path.join(os.getcwd(), 'ffmpeg\\bin')  # 加入环境变量
with open('room.json', 'r') as f:
    room = json.load(f)


class Widget(QWidget):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ma = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(347, 127)
        self.ui.roomE.setText(room['room'])

    @pyqtSlot()
    def on_pushButton_clicked(self):
        roomNum = self.ui.roomE.text().split('/')[-1].split('?')[0]
        if roomNum != '':
            room['room'] = roomNum
            with open('room.json', 'w') as f_obj:
                json.dump(room, f_obj)
            import showMainWindow
            self.ma = showMainWindow.Widget()
            self.ma.show()
            self.close()
        else:
            QMessageBox.information(self, '提示', '未输入房间号')


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    win.show()
    sys.exit(app.exec_())
