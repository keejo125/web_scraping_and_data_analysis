# -*- coding: utf-8 -*-
# author：zhengk

import requests
import json
import re
import jieba.posseg as pseg
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
import os


def get_news_hot(loop=5):
    max_behot_time = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    with open('hot_news.txt', 'w', encoding='utf-8') as f:
        for x in range(loop):
            url = "https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao" \
                  "&widen=1&max_behot_time=" + str(max_behot_time) + "&max_behot_time_tmp=" + str(max_behot_time)
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.text)
                for news in data['data']:
                    f.write(news['title'])
                max_behot_time = data['next']['max_behot_time']


def extract_words():
    with open('hot_news.txt', 'r', encoding='utf-8') as f:
        news_subjects = f.readlines()

    stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))

    news_list = []

    for subject in news_subjects:
        if subject.isspace():
            continue

        p = re.compile("n[a-z0-9]{0,2}")
        word_list = pseg.cut(subject)
        for word, flag in word_list:
            if not word in stop_words and p.search(flag) != None:
                news_list.append(word)

    content = {}
    for item in news_list:
        content[item] = content.get(item, 0) + 1
    return content


def draw_word_cloud(content):
    d = os.path.dirname(__file__)
    img = Image.open(os.path.join(d, "toutiao.jpg"))
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
    plt.savefig("toutiao_wordcloud.png")
    plt.show()


if __name__ == '__main__':
    get_news_hot(5)
    content = extract_words()
    draw_word_cloud(content)
