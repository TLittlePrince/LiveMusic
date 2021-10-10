import sys
import json
import utils
from ui_file.easyDisplayUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication


with open('setting.json', 'r') as f_obj:
    setting = json.load(f_obj)


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = None
        self.open_show = setting['checkBox']
        self.first_font = setting['firstFont']
        self.second_font = setting['secondFont']
        self.first_select = setting['firstSelect']
        self.first_font_size = setting['firstSpin']
        self.win_background = setting['background']
        self.second_select = setting['secondSelect']
        self.second_font_size = setting['secondSpin']
        self.setStyleSheet(f'background-color: {self.win_background}')
        self.ui.label.setStyleSheet(utils.label_style(self.first_font_size, self.first_font, '', self.first_select))
        self.ui.label_2.setStyleSheet(utils.label_style(self.second_font_size, self.second_font, '', self.second_select))

    @pyqtSlot(str)
    def now_play(self, name):
        self.ui.label.setText(name)

    @pyqtSlot(str)
    def next_play(self, name):
        self.ui.label_2.setText(name)

    @pyqtSlot(str)
    def set_now_font(self, font):
        self.ui.label.setStyleSheet(utils.label_style(self.first_font_size, font, '', self.first_select))
        self.first_font = font

    @pyqtSlot(str)
    def set_next_font(self, font):
        self.ui.label_2.setStyleSheet(utils.label_style(self.second_font_size, font, '', self.second_select))
        self.second_font = font

    @pyqtSlot(int)
    def set_now_font_size(self, size):
        self.ui.label.setStyleSheet(utils.label_style(size, self.first_font, '', self.first_select))
        self.first_font_size = size

    @pyqtSlot(int)
    def set_next_font_size(self, size):
        self.ui.label_2.setStyleSheet(utils.label_style(size, self.second_font, '', self.second_select))
        self.second_font_size = size

    @pyqtSlot(str)
    def set_now_font_color(self, color):
        self.ui.label.setStyleSheet(utils.label_style(self.first_font_size, self.first_font, '', color))
        self.first_select = color

    @pyqtSlot(str)
    def set_next_font_color(self, color):
        self.ui.label_2.setStyleSheet(utils.label_style(self.second_font_size, self.second_font, '', color))
        self.second_select = color

    @pyqtSlot(str)
    def set_background_color(self, color):
        self.setStyleSheet(f'background-color: {color}')


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    win.show()
    sys.exit(app.exec_())
