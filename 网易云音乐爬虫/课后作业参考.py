from netease_api import NetEase

singer = '周杰伦'
netEase = NetEase()
songs = netEase.search(singer)

for song in songs['result']['songs']:
    if song['name'] == '告白气球':
        lyric = netEase.getSonglyric(song['id'])
        print(lyric)