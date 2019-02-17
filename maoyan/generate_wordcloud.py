# -*- coding: utf-8 -*-
# author：zhengk
import re


# 输出分词及对应次数
def wordCount():
    import jieba.analyse
    # jieba.load_userdict('../myDict/myDict.txt')
    # jieba.analyse.set_stop_words("../myDict/stop_words.txt")
    word_list=[]
    for line in open('comment.txt'):
        try:
            msg = re.sub("[\s+\.\!\/_,$%^*()+\"\'\?]+|[+——！，。？、~@#￥%……&*（）【】；：]+|\[.+\]|\［.+\］", "", line.split('##')[1])
            tags = jieba.analyse.extract_tags(msg)
            for t in tags:
                word_list.append(t)
        except Exception as e:
            print(e)
    word_dict={}
    for word in word_list:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1
    return word_dict


# 制作图云
def wordCloud(wordList):
    from wordcloud import WordCloud, ImageColorGenerator
    import matplotlib.pyplot as plt
    import numpy as np
    import PIL.Image as Image
    import os
    d = os.path.dirname(__file__)
    img = Image.open(os.path.join(d, "jupiter.png"))
    width = img.width/80
    height = img.height/80
    alice_coloring = np.array(img)
    my_wordcloud = WordCloud(background_color="white",
                             max_words=500, mask=alice_coloring,
                             max_font_size=200, random_state=42,
                             font_path=(os.path.join(d, "../font/msyh.ttf")))
    my_wordcloud = my_wordcloud.generate_from_frequencies(wordList)

    image_colors = ImageColorGenerator(alice_coloring)
    plt.figure(figsize=(width, height))
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    # 通过设置subplots_adjust来控制画面外边框
    plt.subplots_adjust(bottom=.01, top=.99, left=.01, right=.99)
    plt.savefig("jupiter_wordcloud.png")
    plt.show()


if __name__ == '__main__':
    wordList = wordCount()
    wordCloud(wordList)
