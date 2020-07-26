
# -*- coding=utf8 -*-
import matplotlib.pyplot as plt
import jieba.analyse
import numpy
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator


def readTxt(file, encoding='utf-8'):
    """
    :param file:
    :param encoding:
    :return:
    """
    with open(txt_file, 'r', encoding='utf-8') as f:
        txt = f.read()
    return txt

def textDict(content):
    """
    jieba 提取1000个关键词及其比重
    :param content:
    :return:
    """
    result = jieba.analyse.textrank(content, topK=1000, withWeight=True)
    # 转化为比重字典
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]
    return keywords

def renderWordCloud(keywords, sourceImg):
    # 获取图片资源
    image = Image.open(sourceImg)
    # 转为像素矩阵
    graph = numpy.array(image)

    # wordcloud 默认字体库不支持中文，这里自己选取中文字体
    fontPath = 'C:/Windows/Fonts/SIMLI.TTF'
    #fontPath = 'C:/Windows/Fonts/mplus-1mn-regular.ttf'
    wc = WordCloud(
        font_path=fontPath,
        background_color='white',
        max_words=1000,
        # 使用的词云模板背景
        mask=graph
    )
    # 基于关键词信息生成词云
    wc.generate_from_frequencies(keywords)
    # 读取模板图片的颜色
    image_color = ImageColorGenerator(graph)
    # 生成词云图
    plt.imshow(wc)
    # 用模板图片的颜色覆盖
    plt.imshow(wc.recolor(color_func=image_color))
    # 关闭图像坐标系
    plt.axis('off')
    # 显示图片--在窗口显示
    plt.show()


txt_file = '三体.txt'
source_img = 'bac.jpg'
#source_img = 'C:/Users/KF/Pictures/微信图片_20170710102042.jpg'
#source_img = 'C:/Users/KF/Pictures/微信图片_20170710102054.jpg'
#source_img = 'E:\DOC\Carl\wallpapers\d250038c4fde4ea7f36ebe010a7b58ca.jpg'

content = readTxt(txt_file)
keywords = textDict(content)
renderWordCloud(keywords, source_img)