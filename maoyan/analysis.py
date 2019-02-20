# -*- coding: utf-8 -*-
# author：zhengk
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


# 数据分析
def pandas_analysis():
    # 读取评论
    df = pd.read_csv('comment.csv', sep=';', header=None)
    # 整理数据
    df.columns = ['date', 'comment']
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    # 筛选日期
    cacu_df = df[:'2019-02-04']
    # 按日统计数量
    cacu = cacu_df.resample('D').count()
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
    plt.ylabel("评论数", fontproperties=font)

    plt.plot(cacu)
    plt.axis("tight")
    # 显示网格
    plt.grid(True)
    # 自动旋转横轴日期
    plt.gcf().autofmt_xdate()
    # 显示数值
    for a, b in zip(cacu.index, cacu.values):
        plt.text(a, b, str(b[0]))
    # 保存图片
    plt.savefig('comment_analysis.png')
    # 查看图片
    plt.show()


if __name__ == '__main__':
    pandas_analysis()
