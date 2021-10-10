# -*-coding:utf-8-*-
import os
import json
import utils
import base64
import random
import requests
import traceback
from binascii import hexlify
from Crypto.Cipher import AES


headers1 = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'https://music.163.com/#/search/m/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71'
                  ' Safari/537.36 Edg/94.0.992.38',
    'Cookie': '_iuqxldmzr_=32; _ntes_nnid=3781266ef61a5aa2d7ede27aa0183bc1,1551083564434; '
              '_ntes_nuid=3781266ef61a5aa2d7ede27aa0183bc1; WM_TID=OZGc1XNosq1FFVUURUIpkhlLoMCtrNMy; '
              'WM_NI=8rKLP6ufZLsNyeHmP9SDIvgYp6Yeuuu9ZGfzbCvvrI%2B%2FXUYhDsvVVFRPPcN1ekPJXIbE'
              '%2FYcXpJhEf9dT8jQQUfTaONE8iXIYAb%2F6FvZ0Xr4hoDjDHTgTPQpejvbJ0%2FIHU2Q%3D; '
              'WM_NIKE=9ca17ae2e6ffcda170e2e6ee92ef80fbaeb9d8b67b94a88ab2c85e829b9aafee7df'
              '4eda58df544a68f00d7ae2af0fea7c3b92afcae85add33eb7ba96adf246bbbb888ed333919c'
              '8797e653b4ea9786f87fb7e796a8e572a29dba97f143e9f198b6dc6488adbab7d54e9290a08'
              '4cd3ba7b5a0abdb43a29be1bae254b496a8a6e533a88cf88bd45b97ba9c82ce4687e8a7b9cc'
              '5383bee1d7c57e9af09893b764ad9ca6a5cb60a58ca0b2f36faaaaaeabb3258b989bd3d437e2a3; '
              'JSESSIONID-WYYY=%2B0ojNXAeyKT7wKzj1AnD3RXYergSXK5S70VlZwNdlKqvuFDjOfb1Ao2PGtbBU'
              'f38RohOpdmBfcMpY3eM2jp5WiRsaJ22nosm%2F1AwqaJgomKkGAY5VfXyM%2BcVUrlgTEZFHaMNUceP'
              'UXY05Ks23XgW4yr1gPmb%2FJbtbks9nbC0OUlX82cn%3A1551237928176 '
}

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'https://music.163.com/#/search/m/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71'
                  ' Safari/537.36 Edg/94.0.992.38',
    'Cookie': '_iuqxldmzr_=32;_ntes_nnid=6a2d3b7278f578d71b1233125b23c3a0,'
              '1632216503600;_ntes_nuid=6a2d3b7278f578d71b1233125b23c3a0 ;NMTID=00OsaDLkGLz5FOad0B9mnHWx9q1X'
              '-IAAAF8B69Yvw;WNMCID=ovbpoc.1632216504414.01.0;WEVNSM=1.0.0;WM_TID=6LJBRxlzfpRFQBUFFBc%2Bc2qzRAMHmOQC'
              ';JSESSIONID-WYYY=6lvskTjAg5Yu7vf0ktNb6pgoJJTD6hIMctnQKE35RhcCEtFen3DYWnmBAGlos3K7c6enUWxlHJkSdD'
              '%5CY1gnhZ09HX%2F6VU4s0tM5%5CuPCMbERIwwS9yCjdIBk%2BCy6EByPxc1dsAuJTZFrzrEfsmeIQJ3%2B9H1'
              '%2BfqsJZggUHiwIKjWAK4WZh%3A1633706640182;WM_NI=82hf1R6EzpwpeB1F6h2X59YyGlUvu1qStTh0IT5'
              '%2F2kHd0D3sTtKRgxpUexJ3uUItGtZzzBUe%2FhormjsOqfzQSS%2BGt2tG0BUDYdk6u4maLaMq63Hy5xOpCGQzrUIe%2FlEPTUs'
              '%3D;WM_NIKE=9ca17ae2e6ffcda170e2e6ee96ed4aba8a87d9ce4ff1ac8ea7c55b829f8abab5348cb98e82c748989196aaf12'
              'af0fea7c3b92afceea887b45af69bb691f67ca79effa7b564f288fbdadc7385b49b97f83bb38dbcb5eb3c8b8cfbd0b1618cbc'
              '00a5b27998ac85b3e674b48bab99c939b78b8795c6809aa6b6a3d86fedb8a193f062b191bf87f95b918de5a8f73ab89900a3d'
              '8509bbca5d7f840afbf8482d07bf6ed889ab8748db08da8d472b28b8786ae6887909cb6f237e2a3 '
}


def get_random_str():
    str1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_str = ''
    for i in range(16):
        index = random.randint(0, len(str1) - 1)
        random_str += str1[index]
    return random_str


def aes_encrypt(text, key):  # text是要加密的密文，key是密钥
    iv = b'0102030405060708'
    pad = 16 - len(text) % 16
    text = text + chr(2) * pad
    encryptor = AES.new(key.encode(), AES.MODE_CBC, iv)
    encryptor_str = encryptor.encrypt(text.encode())
    result_str = base64.b64encode(encryptor_str).decode()
    return result_str


def rsa_encrypt(text):  # text是16位的随机字符串
    pub_key = '010001'  # js中的e
    # js中的f
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b' \
              '5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e41762' \
              '9ec4ee341f56135fccf695280104e0312ecbda92557c93870114a' \
              'f6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe487' \
              '5d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7 '
    text = text[::-1]
    result = pow(int(hexlify(text.encode()), 16), int(pub_key, 16), int(modulus, 16))
    return format(result, 'x').zfill(131)


# b函数，两次AES加密
def get_aes(text, random_str):
    first_aes = aes_encrypt(text, key='0CoJUm6Qyw8W8jud')  # key是固定的，相当于g
    second_aes = aes_encrypt(first_aes, random_str)
    return second_aes


# 获取加密的参数
def get_post_data(text, random_str):
    params = get_aes(text, random_str)
    encSecKey = rsa_encrypt(random_str)
    return {'params': params, 'encSecKey': encSecKey}


def get_song_list(song_name, random_str):
    # 要加密的字符串
    text = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song_name, "type": "1", "offset": "0",
            "total": "true", "limit": "30", "csrf_token": ""}
    text = json.dumps(text)
    data = get_post_data(text, random_str)
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    # url = 'https://music.163.com/weapi/search/suggest/web?csrf_token='
    return post_requests(url, data)


def post_requests(url, data):
    session = requests.Session()
    session.headers.update(headers)
    re = session.post(url, data=data)
    try:
        re = re.json()
    except json.decoder.JSONDecodeError:
        print(re.text)
        re = {}
    except Exception as e:
        print('发生未知错误')
        traceback.print_exc(file=open('error log.txt', 'a+'))
        print('\ncloudMusicApi.post_request: ' + str(e))
    return re


def get_song_url(song_id, random_str):
    # 'MD 128k': 128000, 'HD 320k': 320000
    text = {'ids': [song_id], 'br': 128000, 'csrf_token': ''}
    text = json.dumps(text)
    data = get_post_data(text, random_str)
    url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
    return post_requests(url, data)


def search(music_name, artist):
    file_name = ''
    music_name = music_name.replace(' ', '%20')  # 音乐名里的空格转成url格式
    random_str = get_random_str()
    music_list = get_song_list(music_name, random_str)
    if music_list != {}:
        # 返回不为空
        music_list = music_list['result']['songs']
        collection = []
        for music_dict in music_list:
            music = music_dict['name']
            # artist = music_dict['ar'][0]['name']
            collection.append(music.upper())
        music_name = music_name.replace('%20', ' ')
        sug = utils.fuzzy_finder(music_name.upper(), collection)
        if sug:
            for music_dict in music_list:
                if sug[0] == music_dict['name'].upper():
                    if artist != '未指定':
                        if (artist in music_dict['ar'][0]['name']) or (
                                artist.upper() in music_dict['ar'][0]['name'].upper()):
                            down(music_dict, random_str)
                            break
                        else:
                            file_name = ''
                    else:
                        file_name = down(music_dict, random_str)
                    break
    return file_name


def down(music_dict, random_str):
    music_id = music_dict['id']
    music_name = music_dict['name']
    artist = music_dict['ar'][0]['name']
    music_url = get_song_url(music_id, random_str)['data'][0]['url']
    if music_url is None:
        file_name = ''
    else:
        file_name = f'{music_name}-{artist}'
        print('正在下载')
        utils.down_load(file_name, music_url)
        print('正在转码')
        utils.mp3_to_wav(f'temp/{file_name}.mp3', f'temp/{file_name}.wav')
        print('成功')
    return file_name


if __name__ == '__main__':
    random_str1 = get_random_str()
    song_name1 = input('输入歌曲名：')
    song_list = get_song_list(song_name1, random_str1)
    id1 = song_list['result']['songs'][0]['id']  # art_name = song_list['result']['songs'][0]['ar'][0]['name']
    song_url = get_song_url(id1, random_str1)['data'][0]['url']
    if not os.path.exists(song_name1):
        os.mkdir(song_name1)  # 新建文件夹
    with open(song_name1 + '/' + song_name1 + '.mp3', 'wb') as f:
        try:
            response = requests.get(song_url, timeout=10)
        except requests.exceptions.ConnectTimeout:  # 超时重新请求
            response = requests.get(song_url, timeout=10)
        f.write(response.content)
