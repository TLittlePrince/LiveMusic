import sys
import atexit
from PyQt5 import sip
from ui_file.addUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QCoreApplication


class Widget(QWidget):
    sinOut = pyqtSignal(str)

    def __init__(self, MName, MArtist, flag1='歌曲', flag2='歌手', parent=None):
        super(Widget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(flag1)
        self.ui.label_2.setText(flag2)
        atexit.register(self.out_emit)
        if flag2 == '':
            sip.delete(self.ui.artistE)
        self.ui.musicE.setText(MName)
        try:
            self.ui.artistE.setText(MArtist)
        except RuntimeError:
            pass

    @pyqtSlot()
    def on_pushButton_clicked(self):
        music = self.ui.musicE.text()
        try:
            artist = self.ui.artistE.text()
        except RuntimeError:
            artist = ''
        if artist == '':
            self.sinOut.emit(f'{music}----未指定')
        else:
            self.sinOut.emit(f'{music}----{artist}')
        self.ui.musicE.clear()
        try:
            self.ui.artistE.clear()
        except RuntimeError:
            pass
        self.close()

    def out_emit(self):
        self.sinOut.emit('')


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget('', '')
    win.show()
    sys.exit(app.exec_())
