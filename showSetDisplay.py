import sys
import json
from ui_file.setEasyDisplayUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QColorDialog
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication, pyqtSignal


with open('setting.json', 'r') as f_obj:
    setting = json.load(f_obj)


class Widget(QWidget):
    sinOut = pyqtSignal(str)

    def __init__(self, obs, parent=None):
        super(Widget, self).__init__(parent)
        self.set = setting
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.obsPlay = obs  # 绿幕显示歌曲名，obs
        self.set_connection()
        self.load_set()

    @pyqtSlot()
    def set_connection(self):
        self.ui.firstSpin.valueChanged.connect(self.save_firstSpin)
        self.ui.secondSpin.valueChanged.connect(self.save_secondSpin)
        self.ui.firstFont.currentTextChanged.connect(self.save_firstFont)
        self.ui.secondFont.currentTextChanged.connect(self.save_secondFont)

    @pyqtSlot()
    def load_set(self):
        first_color = self.set['firstSelect']
        second_color = self.set['secondSelect']
        self.ui.checkBox.setChecked(self.set['checkBox'])
        self.ui.firstSpin.setValue(self.set['firstSpin'])
        self.ui.secondSpin.setValue(self.set['secondSpin'])
        self.ui.firstFont.setCurrentText(self.set['firstFont'])
        self.ui.secondFont.setCurrentText(self.set['secondFont'])
        self.ui.firstSelect.setStyleSheet(f'background-color: {first_color}')
        self.ui.secondSelect.setStyleSheet(f'background-color: {second_color}')

    @pyqtSlot(int)
    def save_firstSpin(self, value):
        self.set['firstSpin'] = value
        self.obsPlay.set_now_font_size(value)

    @pyqtSlot(int)
    def save_secondSpin(self, value):
        self.set['secondSpin'] = value
        self.obsPlay.set_next_font_size(value)

    @pyqtSlot(str)
    def save_firstFont(self, value):
        self.set['firstFont'] = value
        self.obsPlay.set_now_font(value)

    @pyqtSlot(str)
    def save_secondFont(self, value):
        self.set['secondFont'] = value
        self.obsPlay.set_next_font(value)

    @pyqtSlot()
    def on_firstSelect_clicked(self):
        color = QColorDialog.getColor()
        self.set['firstSelect'] = color.name()
        self.obsPlay.set_now_font_color(color.name())
        self.ui.firstSelect.setStyleSheet(f'background-color: {color.name()}')

    @pyqtSlot()
    def on_secondSelect_clicked(self):
        color = QColorDialog.getColor()
        self.set['secondSelect'] = color.name()
        self.obsPlay.set_next_font_color(color.name())
        self.ui.secondSelect.setStyleSheet(f'background-color: {color.name()}')

    @pyqtSlot(bool)
    def on_checkBox_toggled(self, value):
        self.set['checkBox'] = value

    @pyqtSlot()
    def on_setRedB_clicked(self):
        self.set['background'] = 'rgb(255, 0, 0)'
        self.obsPlay.set_background_color('rgb(255, 0, 0)')

    @pyqtSlot()
    def on_setGreenB_clicked(self):
        self.set['background'] = 'rgb(0, 255, 0)'
        self.obsPlay.set_background_color('rgb(0, 255, 0)')

    @pyqtSlot()
    def on_setBuleB_clicked(self):
        self.set['background'] = 'rgb(0, 0, 255)'
        self.obsPlay.set_background_color('rgb(0, 0, 255)')

    @pyqtSlot()
    def on_saveB_clicked(self):
        with open('setting.json', 'w') as f:
            json.dump(self.set, f)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    # win.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
    win.show()
    sys.exit(app.exec_())
