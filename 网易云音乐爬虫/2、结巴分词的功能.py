import jieba


cut = jieba.cut("我和我的祖国，一刻也不能分割")

print(cut)

print(" , ".join(cut))                          # 用 " , " 拼接上cut里面的每一部分
