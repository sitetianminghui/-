# 封装好的 pyc 文件  导入    NetEase
from netease_api import NetEase


netEase = NetEase()


# 第一部分 ：统计 某位歌手所有歌曲的歌曲id(song_id)、歌曲名(song_name)、歌手(singer_name)

singer = 'TFBOYS'                                # 歌手名称 , 用于网易云搜索

# search() 方法 搜索 歌手(singer) , 所有歌曲的相关信息
musics = netEase.search(singer)
# print(musics)


song_count = musics["result"]["songCount"]                   # 统计的歌曲数目
# print(song_count)                                                        # 目前是522首
# print( len(musics["result"]["songs"] ))                            # 只显示了前60首


limit = 30                                                                           # 设置每页歌曲数量最多30首

# 算出页数(page_num)：刚好是每页歌曲数量(limit)的倍数 , 就是算出来的页数 , 有余数的话 , 则页数加1
# 518 / 30 =17.266 不可能为 17.266页，只可能是18页 , 最后一页 8首歌曲
if song_count % limit == 0:
    page_num = int(song_count / limit)
else:
    page_num = int(song_count / limit) + 1


songs = []  # 存放每一首歌的信息
for i in range(16):             # i 等于 0-17页
    print("正在处理", i + 1, "页数据")

    offset = i * limit                             # 每页开始的 偏移量(offset) , 从第多少首歌曲开始爬取

    musics = netEase.search(singer, offset=offset, limit=limit)

    # count : 每页歌曲数目 , 前面17页都是30首一页 , 最后一页歌曲数为8
    if i == page_num - 1:
        count = song_count - offset
    else:
        count = limit

    # 遍历 每一页的 歌曲 , 取出 歌曲ID(song_id)、歌曲名(song_name)、歌手(singer_name)
    for key in range(count):

        song_id = musics["result"]["songs"][key]["id"]

        song_name = musics["result"]["songs"][key]["name"]

        singer_name = musics["result"]["songs"][key]["artists"][0]["name"]

        songs.append([song_id, song_name, singer_name])


# 第二部分：传统方法 过滤 出以下歌手的歌 , 获取歌词并写入文件 , 为下节课准备使用

singer_list = ["TFBOYS","王源","王俊凯","易烊千玺"]

filter_songs = []                                                      # 存放过滤歌手之后的歌手信息

for song in songs:                                                  # 遍历 songs 列表 , 取出其中的每一首歌的信息 
    if song[2] in singer_list:                                      # 把歌手信息取出 , 判断是否在 singer_list   
        filter_songs.append(song)                              # 在的话 , 就把该歌曲信息放到 filter_songs里面   
print("过滤前，歌曲的数目：",len(songs))
print("过滤后，歌曲的数目：",len(filter_songs))




with open('TFBOYS歌词集.txt'  ,'w',encoding='utf-8') as f:
	
	for song in filter_songs:                                                 # 遍历每一首歌 
		
		lyric = netEase.getSonglyric(  song_id=song[0]  )  # 取出 歌曲id , 获取歌词 
		
		if  lyric != None:	                                              # 判断是否有歌词 , 纯音乐是没有的歌词 
			f.write( song[1]+'\n'*2)                                    # 把歌曲名写上 , "\n"*2 ：换2行  
			f.write( lyric + '\n'*5)                                        # 把歌词写上 , "\n"*5： 换5行


"""
# 用 pandas 过滤出以下歌手的歌
import pandas


# 读取 songs 数据转变成表格 ,添加列标题 ["歌曲ID", "歌名", "歌手"]
result = pandas.DataFrame(songs, columns=["歌曲ID", "歌名", "歌手"])
# print(result)


singer_list = ["TFBOYS", "王源", "王俊凯", "易烊千玺"]


# 在result  筛选出 满足 歌手这一列 在 singer_list 里面的歌手
filter_songs = result[result['歌手'].isin(singer_list)]
# print(filter_songs)


# 依次把表格里面 歌曲ID 这一列的每一个数据 , 作为netEase.getSonglyric() 函数的的参数 , 返回的还是一个表格
lyrics = filter_songs['歌曲ID'].map(netEase.getSonglyric)
# print(lyrics)


# 第三部分：提取词组 , 用作字云图像

import jieba                                                     # 结巴分词：用于分开词 , 详情见结巴分词的功能.py
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

null = lyrics[lyrics.isnull()]                             # 筛选出  是空的值(isnull)
# print(null)

not_null = lyrics[~lyrics.isnull()]                    # 筛选出  不是空的值(~...isnull)
# print( not_null )


all_lyric = ''.join(not_null)                                  # 用空格将所有歌词的歌曲连接起来

wordlist_after_jieba = jieba.cut(all_lyric)            # 将歌词分词

wl_space_split = "".join(wordlist_after_jieba)     # 歌词拼接起来
# print(wl_space_split)


user_font = 'simhei.ttf'                                        # 使用字体 , 使得支持中文


wc = WordCloud(font_path=user_font)             # 设置 字体参数
my_word_cloud = wc.generate(wl_space_split)    # 对歌词生成字云


plt.imshow(my_word_cloud)

plt.axis("off")                                 # off(关闭) 坐标轴线(axis)

plt.show()


# # 扩展：可选择用图片做背景生成字云
import numpy
from PIL import Image


# 读取图片将组成的RGB数值 ,  转换成数组(array)
alice_coloring = numpy.array(Image.open("holmes.png"))
# print(alice_coloring)


#                              背景颜色                         最大字数              掩饰面具                     最大字体                 随机范围              字体
wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring, max_font_size=40, random_state=42, font_path=user_font)
my_word_cloud = wc.generate(wl_space_split)


#                        图片  颜色   生成器       颜色数据
image_colors = ImageColorGenerator(alice_coloring)

#                                         重设颜色
plt.imshow(my_word_cloud.recolor(color_func=image_colors))


plt.imshow(my_word_cloud)

plt.axis("off")

plt.savefig('test2.tif', dpi=4000, bbox_inches='tight')     # 保存图片

plt.show()

"""