# -*- coding: utf-8 -*-
# author：zhengk

import pandas as pd
from matplotlib.font_manager import FontProperties
import jieba.posseg as pseg
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
import os
import re


def extract_words(comment_df):
    stop_words = set(line.strip() for line in open('../common/stopwords.txt', encoding='utf-8'))
    news_list = []
    for item in comment_df.itertuples(index=False):
        comment = item.comment.replace(' ','')
        if comment.isspace():
            continue
        p = re.compile("n[a-z0-9]{0,2}")
        word_list = pseg.cut(comment)
        for word, flag in word_list:
            if not word in stop_words and p.search(flag) != None:
                news_list.append(word)
    content = {}
    for item in news_list:
        content[item] = content.get(item, 0) + 1
    return content


def draw_word_cloud(content):
    d = os.path.dirname(__file__)
    img = Image.open(os.path.join(d, "changzuoren.jpg"))
    width = img.width / 80
    height = img.height / 80
    alice_coloring = np.array(img)
    my_wordcloud = WordCloud(background_color="white",
                             max_words=500, mask=alice_coloring,
                             max_font_size=200, random_state=42,
                             font_path=(os.path.join(d, "../common/font/PingFang.ttc")))
    my_wordcloud = my_wordcloud.generate_from_frequencies(content)

    image_colors = ImageColorGenerator(alice_coloring)
    plt.figure(figsize=(width, height))
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    # 通过设置subplots_adjust来控制画面外边框
    plt.subplots_adjust(bottom=.01, top=.99, left=.01, right=.99)
    plt.savefig("changzuoren_wordcloud.png")
    plt.show()


def gender_analysis(gender_df):
    # 通过设置中文字体方式解决中文展示问题
    font = FontProperties(fname='../common/font/PingFang.ttc')

    gender_df.drop_duplicates()
    gender_df['gender'].replace({0: 'man', 1: 'female'}, inplace=True)
    g_df = gender_df.groupby(['gender']).count()
    g_df.plot(kind='bar', legend=False)
    plt.title("我是唱作人观众性别分析", fontproperties=font)
    plt.xlabel("性别", fontproperties=font)
    plt.ylabel("人数", fontproperties=font)
    plt.xticks(rotation=360)
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('comments.csv', sep=';', header=None)
    df.columns = ['date', 'nickname', 'gender', 'comment']
    gender_df = df[['nickname', 'gender']]
    gender_analysis(gender_df)
    comment_df = df[['comment']]
    content = extract_words(comment_df)
    draw_word_cloud(content)
