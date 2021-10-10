import os
import sys
import json
import time
import utils
import useAdd
import kuWoApi
import showHTML
import threading
import traceback
import displayOn
import showAbout
import main_class
import cloudMusicApi
import displayQRCode
# from CUi import Ui_Form
from ui_file.MainWindowCUI import Ui_MainWindow
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPoint, pyqtSlot, pyqtSignal, QCoreApplication

stop = True  # 停止列表播放
with open('BlackList.json', 'r') as f:
    bl = json.load(f)
pt = os.getcwd()
ph = pt.split('\\')
del ph[-1]
ph = '/'.join(ph)
os.chdir(ph)
ph = ph.split('/')
ph.append('Update.exe')
ph = '/'.join(ph)
os.system(ph)
os.chdir(pt)


class Widget(QMainWindow):  # QWidget):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        # self.ui = Ui_Form()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.row = 0  # 选中的位置
        self.th = None  # 播放进程
        self.add = None  # 添加/修改面板
        self.ban = None  # 黑名单列表
        self.list_row = 0  # 总共的数量
        self.ban_music = bl  # 音乐黑名单
        self.playFlag = True  # 执行播放还是暂停
        self.cold_down = None  # 设置冷却时间
        self.setDisplay = None  # 显示设置
        self.change_vol = None  # 设置音量
        self.how_to_use = None  # 如何使用
        self.QR = displayQRCode.Widget()  # 二维码
        self.about_widget = showAbout.Widget()  # 关于面板
        self.obsPlay = displayOn.Widget()  # 绿幕显示歌曲名，obs
        self.Th = main_class.RoomWorker()  # 维持房间连接
        self.Th2 = main_class.DanMuWorker()  # 弹幕
        self.Th2.sinOut.connect(self.append_on)  # 自动加入列表
        self.ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(self.add_menu)

    @pyqtSlot(str)
    def write_str(self, music_str):
        # 手动修改
        self.ui.listWidget.item(self.row).setText(music_str)
        self.add.sinOut.disconnect(self.write_str)
        self.add.sinOut.connect(self.append_on_str)

    @pyqtSlot(str)
    def append_on_str(self, music_str):
        # 手动加入
        if music_str != '':
            print(music_str)
            self.ui.listWidget.addItem(music_str)
        else:
            self.add.sinOut.disconnect(self.write_str)
            self.add.sinOut.connect(self.append_on_str)
        self.list_row += 1
        try:
            self.obsPlay.next_play(self.ui.listWidget.item(0).text())
        except AttributeError:
            self.obsPlay.next_play('')

    @pyqtSlot(list)
    def append_on(self, music_list):
        # 加入队列自动加入
        print(music_list)
        try:
            self.ui.listWidget.addItem(f'{music_list[0]}----{music_list[1]}')
        except IndexError:
            self.ui.listWidget.addItem(f'{music_list[0]}----未指定')
        self.list_row += 1
        """if self.list_row == 1:
            self.play_next('done')"""
        try:
            self.obsPlay.next_play(self.ui.listWidget.item(0).text())
        except AttributeError:
            self.obsPlay.next_play('')
        pass

    @pyqtSlot(QPoint)
    def add_menu(self, pos):
        # 表格右键删除菜单
        menu = QMenu()
        listAdd = menu.addAction('添加')
        listWrite = menu.addAction('修改')
        listDel = menu.addAction('删除')
        listAddBlack = menu.addAction('添加到黑名单')
        # moneySupport = menu.addAction('支持作者')
        action = menu.exec_(self.ui.listWidget.mapToGlobal(pos))
        try:
            try:
                strN = self.ui.listWidget.item(self.row).text().split('----')
            except AttributeError:
                strN = ['', '']
            name = strN[0]
            art = strN[1]
            self.add = useAdd.Widget(name, art)
            self.add.sinOut.connect(self.append_on_str)
            self.row = self.ui.listWidget.selectionModel().selection().indexes()[-1].row()
            if action == listDel:
                s = self.ui.listWidget.takeItem(self.row)
                try:
                    self.obsPlay.next_play(self.ui.listWidget.item(0).text())
                except AttributeError:
                    self.obsPlay.next_play('')
                print(s.text())
                self.list_row -= 1
            elif action == listAdd:
                self.add.show()
            elif action == listWrite:
                self.add.sinOut.disconnect(self.append_on_str)
                self.add.sinOut.connect(self.write_str)
                self.add.show()
            elif action == listAddBlack:
                ban = self.ui.listWidget.item(self.row).text().split('----')[0]
                self.ban_music.append(ban)
                with open('BlackList.json', 'w') as f_obj:
                    json.dump(self.ban_music, f_obj)
            """elif action == moneySupport:
                self.QR.show()
                pass"""
        except IndexError:
            if action == listAdd:
                self.add.show()
            """elif action == moneySupport:
                self.QR.show()
                pass"""
        except Exception as e:
            traceback.print_exc(file=open('error log.txt', 'a+'))
            print('\nmain.add_menu: ' + str(e))

    @pyqtSlot()
    def load_music(self):
        # 自动播放歌曲
        with open('setting.json', 'r') as f_obj:
            utils.change_vol(json.load(f_obj))
        while stop:
            try:
                with open('BlackList.json', 'r') as f_obj:
                    self.ban_music = json.load(f_obj)
                music_info = self.ui.listWidget.takeItem(0).text().split('----')
                # music_info = music_info[0].replace('/', ' '), music_info[1].replace('/', ' ')
                if music_info[0] not in self.ban_music:
                    if music_info[0] == '麻雀学校':
                        file_name = kuWoApi.search(music_info[0], music_info[1])
                    else:
                        try:
                            file_name = cloudMusicApi.search(music_info[0], music_info[1])
                        except KeyError:
                            time.sleep(2)
                            file_name = cloudMusicApi.search(music_info[0], music_info[1])
                        if file_name == '':
                            file_name = kuWoApi.search(music_info[0], music_info[1])
                    if file_name != '':
                        self.playFlag = False
                        self.ui.nowPlayLabel.setText(f'现在播放：{file_name}')
                        self.obsPlay.now_play(f'{file_name}')
                        try:
                            self.obsPlay.next_play(self.ui.listWidget.item(0).text())
                        except AttributeError:
                            self.obsPlay.next_play('')
                        utils.mp3_player(f'temp/{file_name}.wav')
                        os.remove(f'temp/{file_name}.wav')
                    else:
                        print('\n未找到符合的歌曲\n')
                else:
                    print('提醒：指定的歌曲在黑名单中')
                    time.sleep(1)
            except AttributeError:
                self.ui.nowPlayLabel.setText('当前无歌曲')
                self.obsPlay.now_play('当前无歌曲')
                self.obsPlay.next_play('当前无歌曲')
                time.sleep(1)
            except OSError:
                print('\n提示:未检测到音频设备\n')
                pass
            except Exception as e:
                traceback.print_exc(file=open('error log.txt', 'a+'))
                print('\nmain.load_music: ' + str(e))
        self.th = threading.Thread(target=self.load_music)
        self.th.daemon = 1
        self.th.start()

    @pyqtSlot(str)
    def play_next(self, name):
        # 第一首开启歌曲自动播放
        print(name)
        self.th = threading.Thread(target=self.load_music)
        self.th.daemon = 1
        self.th.start()

    @pyqtSlot()
    def on_startB_clicked(self):
        # 弹幕获取
        self.Th.daemon = 1
        self.Th2.daemon = 1
        self.Th.start()
        self.Th2.start()
        self.play_next('done')
        self.ui.startB.setText('正在统计中~')
        with open('setting.json', 'r') as f_obj:
            flag = json.load(f_obj)
        if flag['checkBox'] and not flag['open']:
            self.obsPlay.show()

    @pyqtSlot()
    def on_playB_clicked(self):
        # 播放/暂停
        if self.playFlag:
            utils.stopFlag = False
            self.playFlag = False
            self.ui.playB.setText('暂停')
        else:
            utils.stopFlag = True
            self.playFlag = True
            self.ui.playB.setText('播放')

    @pyqtSlot()
    def on_nextMusicB_clicked(self):
        # 下一首
        utils.stopFlag = False
        self.playFlag = False
        self.ui.playB.setText('暂停')
        utils.killFlag = True

    @pyqtSlot()
    def on_clearB_clicked(self):
        self.ui.listWidget.clear()
        self.obsPlay.next_play('')

    @pyqtSlot()
    def on_actionVol_triggered(self):
        import showChangeVol
        self.change_vol = showChangeVol.Widget()
        self.change_vol.show()

    @pyqtSlot()
    def on_actionMusic_triggered(self):
        import useBlackList
        self.ban = useBlackList.Widget('歌曲黑名单', 'BlackList')
        self.ban.show()

    @pyqtSlot()
    def on_actionUser_triggered(self):
        import useBlackList
        self.ban = useBlackList.Widget('用户黑名单', 'BlackUserList')
        self.ban.show()

    @pyqtSlot()
    def on_actionColdDown_triggered(self):
        import showColdDown
        self.cold_down = showColdDown.Widget()
        self.cold_down.show()

    @pyqtSlot()
    def on_actionLive_triggered(self):
        import showSetDisplay
        with open('setting.json', 'r') as f_obj:
            flag = json.load(f_obj)
        if flag['open']:
            self.setDisplay = showSetDisplay.Widget(self.obsPlay)
            self.setDisplay.show()
            flag['open'] = False
        with open('setting.json', 'w') as f_obj:
            json.dump(flag, f_obj)
        self.obsPlay.show()

    @pyqtSlot()
    def on_actionSetDisplay_triggered(self):
        import showSetDisplay
        self.setDisplay = showSetDisplay.Widget(self.obsPlay)
        self.setDisplay.show()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        self.about_widget.show()

    @pyqtSlot()
    def on_actionSupport_triggered(self):
        self.QR.show()

    @pyqtSlot()
    def on_actionHowToUse_triggered(self):
        self.how_to_use = showHTML.Widget()
        self.how_to_use.show()
        pass


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Widget()
    win.show()
    sys.exit(app.exec_())
