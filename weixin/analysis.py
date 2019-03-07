# -*- coding: utf-8 -*-
# author：zhengk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from matplotlib.font_manager import FontProperties


def timeline_plot():
    df_ori = pd.read_csv('articles.csv', sep=';', header=None)

    # 取第一列并分割日期与标题
    df = df_ori.iloc[:, 0]
    df = df.str.split(';', expand=True)

    # 格式化日期，设置column，并将日期设置为index
    df.columns = ['date', 'title']
    df.date = pd.to_datetime(df.date)
    df = df.set_index('date')

    # 按月统计文章数"MS"为月初
    cacu = df.resample("MS").count()

    # 画图
    fig, ax = plt.subplots(figsize=[18, 5])

    # 线条
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
    ax.plot(cacu, 'o-')

    # fig.autofmt_xdate()

    # 通过设置中文字体方式解决中文展示问题
    font = FontProperties(fname='../font/PingFang.ttc', size=18)
    ax.set_title("新世相文章统计", fontproperties=font)
    ax.set_xlabel("日期", fontproperties=font)
    ax.set_ylabel("文章数", fontproperties=font)

    # 设置时间轴
    formater = mdate.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(formater)
    ax.xaxis.set_minor_locator(mdate.MonthLocator())
    ax.xaxis.set_minor_formatter(mdate.DateFormatter('%m'))
    ax.xaxis.set_major_locator(mdate.YearLocator())
    ax.xaxis.set_major_formatter(mdate.DateFormatter('\n\n%Y'))
    # 显示网格
    # ax.xaxis.grid(True, which="minor")
    # ax.yaxis.grid()
    # 显示数值
    # 显示全部数值
    # for a,b in zip(cacu.index, cacu.values):
    #     ax.text(a, b, b[0])
    # 显示最大值
    x = cacu['title'].idxmax()
    y = cacu['title'].max()
    ax.text(x, y, y, verticalalignment='bottom', horizontalalignment='center', fontsize='large')
    # plt.annotate(y, xy=(x,y))
    # 保存图片
    plt.savefig('timeline_analysis.png')
    # 显示图片
    plt.show()


if __name__ == '__main__':
    timeline_plot()
