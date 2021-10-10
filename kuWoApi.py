import json
import time
import utils
import requests
import traceback


def ku_wo_api(music_name):
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
        "Cookie": "_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; "
                  "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; "
                  "Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P",
        "Referer": "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
        "csrf": "HYZQI4KPK3P",
    }
    # 参数列表
    params = {
        "key": music_name,
        # 页数
        "pn": "1",
        # 音乐数
        "rn": "10",
        "httpsStatus": "1",
        "reqId": "cc337fa0-e856-11ea-8e2d-ab61b365fb50",
    }
    # 创建列表,后面下载需要
    music_list = []
    url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
    res = requests.get(url=url, headers=headers, params=params)
    res.encoding = "utf-8"
    text = res.text
    # 转成json数据
    json_list = json.loads(text)
    # 发现data中list是存主要数据的地方
    try:
        dataPack = json_list["data"]["list"]
    except Exception as e:
        print('发生未知错误')
        traceback.print_exc(file=open('error log.txt', 'a+'))
        print('\nkuWoApi.ku_wo_api.dataPack: ' + str(e))
        dataPack = []
    # 遍历拿到所需要的数据，音乐名称，歌手，id...
    for i in dataPack:
        # 音乐名
        music_name = i["name"]
        # 歌手
        music_singer = i["artist"]
        # 待会需要的id先拿到
        rid = i["rid"]
        # 随便试听拿到一个音乐的接口,这是的rid就用得上了
        api_music = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3" \
                    "&br=128kmp3&from=web&t=1598528574799&httpsStatus=1" \
                    "&reqId=72259df1-e85a-11ea-a367-b5a64c5660e5".format(rid)
        api_res = requests.get(url=api_music)
        # 打印发现真实的url确实在里面
        # print(api_res.text)
        try:
            music_url = json.loads(api_res.text)["url"]
        except json.decoder.JSONDecodeError:
            continue
        except Exception as e:
            music_url = ''
            print('发生未知错误')
            traceback.print_exc(file=open('error log.txt', 'a+'))
            print('\nkuWoApi.ku_wo_api.music_url: ' + str(e))
        # 大功告成，试试效果
        print(music_name)
        print(music_singer)
        print(music_url)
        # 把数据存到字典方便下载时查找
        music_dict = {"name": music_name, "url": music_url, "singer": music_singer}
        music_list.append(music_dict)
    # 看看真实数据数量
    print(len(music_list))
    return music_list


def search(music_name, artist):
    music_list = []
    file_name = ''
    # 使用酷我音乐
    try:
        music_list = ku_wo_api(music_name)
    except json.decoder.JSONDecodeError:
        print('网页解析错误，正在重试')
        time.sleep(1)
        music_list = ku_wo_api(music_name)
        pass
    except KeyError:
        print('键错误，正在重试')
        time.sleep(1)
        music_list = ku_wo_api(music_name)
    except Exception as e:
        print('发生未知错误', 2)
        traceback.print_exc(file=open('error log.txt', 'a+'))
        print('\nkuWoApi.search.music_list: ' + str(e))
    for info in music_list:
        if artist != '未指定':
            if ((info['name'] == music_name) or
                (info['name'].upper() == music_name.upper())) and \
                    ((artist in info['singer']) or
                     (artist.upper() in info['singer'].upper())):
                file_name = f'{music_name}-{artist}'
                print('正在下载')
                utils.down_load(file_name, info['url'])
                print('正在转码')
                utils.mp3_to_wav(f'temp/{file_name}.mp3', f'temp/{file_name}.wav')
                print('成功')
                break
        else:
            if ((info['name'] == music_name) or
                    (info['name'].upper() == music_name.upper())):
                artist = info['singer']
                file_name = f'{music_name}-{artist}'
                print('正在下载')
                utils.down_load(file_name, info['url'])
                print('正在转码')
                utils.mp3_to_wav(f'temp/{file_name}.mp3', f'temp/{file_name}.wav')
                print('成功')
                break
    return file_name
