# 封装好的 pyc 文件  导入    NetEase
from netease_api import NetEase


netEase = NetEase()

# netEase:网易云
# song:歌
# search:搜索，搜索歌手唱过的哥
# lyric:歌词

# 第一部分 ：  getSonglyric()方法 和 search() 方法

# getSonglyric()方法 ：获取歌词(lyric) , 传入 song_id 就可以获得歌词
geci = netEase.getSonglyric(song_id=1407216008)

# print(geci)


singer = 'TFBOYS'                       # 歌手

# search() 方法 搜索 歌手(singer) , 获得歌手的相关信息
# 默认stype=1 单曲 , stype=10 专辑 , stype=100歌手 , stype=1000 歌单
musics = netEase.search(singer, stype=1)

# print(musics)


# 利用for 循环 把 musics 的每一部分找出来

for i in musics["result"]["songs"]:
    print(i["artists"][0]["name"])


song_count = musics["result"]["songCount"]                   # 统计的歌曲数目
print(song_count)

# 
songs = musics['result']['songs']
for song in songs:
    print(song['id'],song['name'],song['artists'][0]['name'])


a = netEase.getCommentNum(566442223)
# total是总数
print("评论总数是:"+str(a["total"]))
# hotComment:热评(热门评论)
hc = a["hotComments"]
for i in hc:
    print(i['user']['nickname'],i["likedCount"],i['content'])