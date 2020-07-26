# 第三部分：提取词组 , 用作字云图像
import jieba                                                     # 结巴分词：用于分开词 , 详情见结巴分词的功能.py
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

with open('TFBOYS歌词集.txt','r',encoding='utf-8')as f:
    
    all_lyric = f.read()                              # 用空格将所有歌词的歌曲连接起来

wordlist_after_jieba = jieba.cut(all_lyric)            # 将歌词分词

wl_space_split = "".join(wordlist_after_jieba)     # 歌词拼接起来
# print(wl_space_split)


user_font = 'simhei.ttf'                                        # 使用字体 , 使得支持中文


wc = WordCloud(font_path=user_font)             # 设置 字体参数
my_word_cloud = wc.generate(wl_space_split)    # 对歌词生成字云


plt.imshow(my_word_cloud)

plt.axis("off")                                 # off(关闭) 坐标轴线(axis)

plt.show()

'''
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
'''

# plt.savefig('test2.tif', dpi=4000, bbox_inches='tight')     # 保存图片

# plt.show()
