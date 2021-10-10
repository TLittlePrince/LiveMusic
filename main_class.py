import time
import json
import asyncio
import traceback
import threading
from bilibili_api import sync, exceptions
from bilibili_api.live import LiveDanmaku
from PyQt5.QtCore import QThread, pyqtSignal

with open('room.json', 'r') as f:
    room = json.load(f)

dan_mu_msg = []  # 待传歌曲列表
user_count_down = []  # 用户点歌缓冲区，一段时间内不能点歌，计时结束后移出列表
num = 0
pass_key = 'flzxsqc'
room1 = LiveDanmaku(room_display_id=room['room'])


# 弹幕
@room1.on("DANMU_MSG")  # 指定事件名
async def on_dan_mu(msg_json):
    global num
    user = msg_json['data']['info'][2][1]  # 用户名
    com = msg_json['data']['info'][1]  # 弹幕内容
    te_com = com.split('#')[-1]
    com = com.split('#')[0]
    com = com.split(' ', 1)
    if te_com == pass_key[num]:
        append_on(com, user, flag=False)
        num += 1
        if num > 6:
            num = 0
    else:
        with open('BlackUserList.json', 'r') as f_obj:
            ban_user_list = json.load(f_obj)
        try:
            if user not in user_count_down and user not in ban_user_list:
                append_on(com, user)
        except IndexError:
            pass
        except Exception as e:
            traceback.print_exc(file=open('error log.txt', 'a+'))
            print('\nmain_class.on_dan_mu: ' + str(e))


def append_on(com, user, flag=True):
    if com[0] == '点歌' or com[0] == '.':
        if com[1] != '':
            music_info = com[1].split('&')
            try:
                name = music_info[0].replace('*', '')
                artist = music_info[1].replace('*', '')
                name = name.lstrip().rstrip()
                artist = artist.lstrip().rstrip()
                dan_mu_msg.append([name, artist])  # 去除非法字符
                if flag:
                    t = UserTimer(user)
                    t.start()  # 开始计时
            except IndexError:
                try:
                    name = music_info[0].replace('*', '')
                    name = name.lstrip().rstrip()
                    dan_mu_msg.append([name])  # 去除非法字符
                    if flag:
                        t = UserTimer(user)
                        t.start()  # 开始计时
                except IndexError:
                    pass


class UserTimer(threading.Thread):

    def __init__(self, username, parent=None):
        super(UserTimer, self).__init__(parent)
        self.working = True
        self.username = username

    def run(self):
        user_count_down.append(self.username)
        with open('setting.json', 'r') as f_obj:
            times = json.load(f_obj)['time']
        time.sleep(times*60)
        user_count_down.remove(self.username)


class RoomWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RoomWorker, self).__init__(parent)
        # 设置工作状态与初始num数值
        self.working = True
        self.num = 1

    def run(self):
        global room1
        print("start connect")
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.num = 0
        try:
            sync(room1.connect())
        except (exceptions.LiveException.LiveException, RuntimeError):
            self.num = 1


class DanMuWorker(QThread):
    sinOut = pyqtSignal(list)

    def __init__(self, parent=None):
        super(DanMuWorker, self).__init__(parent)
        # 设置工作状态与初始num数值
        self.working = True
        self.num = 0

    def run(self):
        global room
        while self.working:
            with open('room.json', 'r') as f_obj:
                room = json.load(f_obj)
            time.sleep(0.5)
            if dan_mu_msg:
                for music_name_list in dan_mu_msg:
                    self.sinOut.emit(music_name_list)
                    dan_mu_msg.remove(music_name_list)
