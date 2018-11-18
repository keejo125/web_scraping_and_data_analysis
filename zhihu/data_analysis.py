# -*- coding: utf-8 -*-
import pandas as pd

fieldnames = ['question', 'answer', 'voteup']
df = pd.read_csv('topic_top_answer.csv',encoding = "utf-8",header = None, names =fieldnames)  #打开表格

# 筛选回答字数少于20，按点赞从高往低排列
df_genius_answers = df[df.answer.str.len() < 20].sort_values(by='voteup', ascending=False)

# 输出到xls
df_genius_answers.to_excel('genius_answers.xls', index=False)
print(df_genius_answers[['question', 'answer', 'voteup']])

