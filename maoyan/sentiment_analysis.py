# -*- coding: utf-8 -*-
# author：zhengk
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


def sentiments_analysis():
    from snownlp import SnowNLP
    # 读取评论
    df = pd.read_csv('comment.csv', sep=';', header=None)
    # 获取情感评分
    sentiment = lambda x:SnowNLP(x).sentiments
    df[2] = df[1].apply(sentiment)
    # 写入csv
    # df.to_csv('comment_sentiments.csv', sep=';', index=False, header=False)
    # 整理数据
    df.columns = ['date', 'comment', 'sentiment']
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    # 筛选日期
    cacu_df = df[:'2019-02-04']['sentiment']
    # 按日统计数量
    cacu = cacu_df.resample('D').mean()
    # 画图
    # 使用plot画pandas建议先注册
    register_matplotlib_converters()

    # 使用pltz解决中文展示问题
    # 新建pltz对象，用于显示中文
    # from pyplotz.pyplotz import PyplotZ
    # pltz = PyplotZ()
    # pltz.enable_chinese()
    # pltz.title("流浪地球评论分析")
    # pltz.xlabel("日期")
    # pltz.ylabel("评论数")

    # 通过设置中文字体方式解决中文展示问题
    font = FontProperties(fname='../font/PingFang.ttc')
    plt.title("流浪地球评论分析", fontproperties=font)
    plt.xlabel("日期", fontproperties=font)
    plt.ylabel("好感度", fontproperties=font)

    plt.plot(cacu)
    plt.axis("tight")
    # 显示网格
    plt.grid(True)
    # 自动旋转横轴日期
    plt.gcf().autofmt_xdate()
    # 显示数值
    for a, b in zip(cacu.index, cacu.values):
        plt.text(a, b, str(round(b, 4)))
    # 保存图片
    plt.savefig('comment_sentiment_analysis.png')
    # 查看图片
    plt.show()


if __name__ == '__main__':
    sentiments_analysis()
