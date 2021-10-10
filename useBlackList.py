import sys
import json
import useAdd
import traceback
from ui_file.blackListUI import Ui_Form
from PyQt5.QtWidgets import QMenu, QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, pyqtSlot, QCoreApplication


class Widget(QWidget):

    def __init__(self, title, path, parent=None):
        super(Widget, self).__init__(parent)
        self.row = 0
        self.ui = Ui_Form()
        self.path = path
        with open(f'{self.path}.json', 'r') as f:
            self.ban_music = json.load(f)
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        if title == '用户黑名单':
            self.add = useAdd.Widget('', '', flag1='用户名', flag2='')
        else:
            self.add = useAdd.Widget('', '')
        self.add.sinOut.connect(self.append_on_str)
        self.ui.listWidget.addItems(self.ban_music)
        self.ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(self.add_menu)

    @pyqtSlot(QPoint)
    def add_menu(self, pos):
        # 表格右键删除菜单
        menu = QMenu()
        listAdd = menu.addAction('添加')
        listWrite = menu.addAction('修改')
        listDel = menu.addAction('删除')
        action = menu.exec_(self.ui.listWidget.mapToGlobal(pos))
        try:
            self.row = self.ui.listWidget.selectionModel().selection().indexes()[-1].row()
            self.add = useAdd.Widget(self.ui.listWidget.item(self.row).text(), '')
            self.add.sinOut.connect(self.append_on_str)
            if action == listDel:
                # 删除
                s = self.ui.listWidget.takeItem(self.row)
                print(s.text())
                ban = s.text().split('----')[0]
                self.ban_music.remove(ban)
                with open(f'{self.path}.json', 'w') as f_obj:
                    json.dump(self.ban_music, f_obj)
                # self.list_row -= 1
            elif action == listAdd:
                # 添加
                self.add.show()
            elif action == listWrite:
                # 修改
                self.add.sinOut.disconnect(self.append_on_str)
                self.add.sinOut.connect(self.write_str)
                self.add.show()
                pass
        except IndexError:
            if action == listAdd:
                # 添加
                self.add.show()
        except Exception as e:
            traceback.print_exc(file=open('error log.txt', 'a+'))
            print('\nuseBlackList.add_menu: ' + str(e))

    @pyqtSlot(str)
    def write_str(self, music_str):
        self.ui.listWidget.item(self.row).setText(music_str)
        self.add.sinOut.disconnect(self.write_str)
        self.add.sinOut.connect(self.append_on_str)

    @pyqtSlot(str)
    def append_on_str(self, music_str):
        if music_str != '':
            if music_str not in self.ban_music:
                print(music_str)
                self.ban_music.append(music_str.split('----')[0])
                self.ui.listWidget.addItem(music_str.split('----')[0])
                with open(f'{self.path}.json', 'w') as f_obj:
                    json.dump(self.ban_music, f_obj)
        else:
            self.add.sinOut.disconnect(self.write_str)
            self.add.sinOut.connect(self.append_on_str)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    # win.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
    win.show()
    sys.exit(app.exec_())
