# coding:utf-8
# uncompyle6 version 3.4.1
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.7.1 (default, Dec 10 2018, 22:54:23) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: /Users/apple/Desktop/L19_生成歌词/netease_api.py
# Compiled at: 2018-04-12 16:34:40
# Size of source mod 2**32: 6891 bytes
import os
import json
import re
import hashlib
import base64
import binascii
from Crypto.Cipher import AES
import requests
import prettytable
default_timeout = 100
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


def encrypted_id(id):
    magic = bytearray('3go8&$8*3*3h0k(2)2', 'u8')
    song_id = bytearray(id, 'cd u8')
    magic_len = len(magic)
    for i, sid in enumerate(song_id):
        song_id[i] = sid ^ magic[(i % magic_len)]

    m = hashlib.md5(song_id)
    result = m.digest()
    result = base64.b64encode(result)
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result.decode('utf-8')


def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    return data


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return binascii.hexlify(os.urandom(size))[:16]


def readLyric(filename):
    with open(filename, 'r') as (f):
        f.read()


class NetEase:

    def __init__(self):
        self.header = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip,deflate,sdch',
                       'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
                       'Connection': 'keep-alive',
                       'Content-Type': 'application/x-www-form-urlencoded',
                       'Host': 'music.163.com',
                       'Referer': 'http://music.163.com/search/',
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'}
        self.cookies = {'appver': '1.5.2'}

    def search(self, s, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get/web'
        data = {'s': s,
                'type': stype,
                'offset': offset,
                'total': total,
                'limit': limit}
        return self.httpRequest('POST', action, data)

    def httpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        if method == 'GET':
            url = action if query == None else action + '?' + query
            connection = requests.get(url, headers=(self.header), timeout=default_timeout)
        else:
            connection = requests.post(action,
                                       data=query,
                                       headers=(self.header),
                                       timeout=default_timeout)
        connection.encoding = 'UTF-8'
        connection = json.loads(connection.text)
        return connection

    def getCommentNum(self, id):
        action = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(id) + '?csrf_token='
        csrf = ''
        req = {'csrf_token': csrf}
        data = encrypted_request(req)
        return self.httpRequest('POST', action, data)

    def getSongcount(self, singer):
        result = self.search(singer)
        return result['result']['songCount']

    def getAllsongs(self, singer, limit, isprint=True):
        songCount = self.getSongcount(singer)
        pageNum = int(songCount / limit) if songCount % limit == 0 else int(songCount / limit) + 1
        songs = []
        for currentPage in range(pageNum):
            print('正在处理第' + str(currentPage + 1) + '页数据...')
            offset = currentPage * limit
            musics = self.search(singer, stype=1, offset=offset, limit=limit)
            count = songCount - offset if currentPage == pageNum - 1 else limit
            for key in range(count):
                songId = musics['result']['songs'][key]['id']
                songName = musics['result']['songs'][key]['name']
                result = self.getCommentNum(songId)
                commentNum = result['total']
                singer_name = musics['result']['songs'][key]['artists'][0]['name']
                songs.append([songId, songName, singer_name, commentNum])

        if isprint:
            fields = [
             'NO.', 'ID', '歌名', '歌手', '评论数量']
            self.printTable(fields, songs)
        return songs

    def printTable(self, fields, songs):
        table = prettytable.PrettyTable()
        table.field_names = fields
        for number in range(len(songs)):
            table.add_row([number + 1, songs[number][0], songs[number][1], songs[number][2], songs[number][3]])

        print(table)

    def getSonglyric(self, song_id):
        action = 'http://music.163.com/api/song/lyric?id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
        lyric = self.httpRequest('GET', action)
        if 'lrc' in lyric.keys():
            lrc = lyric['lrc']['lyric']
            pat = re.compile('\\[.*\\]')
            lrc = re.sub(pat, '', lrc)
            lrc = lrc.strip()
            return lrc
        else:
            return


def filter_txt(txt):
    import re
    pattern = re.compile(".+(?<!['源','玺','凯','合','唱'])[:,：].+")
    x = [re.sub(pattern, '', s) for s in txt]
    pattern2 = re.compile(".*(?<=['源','玺','凯','合','唱'])[:,：]?")
    x = [re.sub(pattern2, '', s) for s in x]
    x = [re.sub("[A-Za-z0-9\\(\\)\\（\\）\\'\\~\\.\\:\\：\\!]", '', s) for s in x]
    lyric = [re.sub('(?<=\\n)\\s+', '', s) for s in x]
    return lyric
# okay decompiling netease_api.pyc
