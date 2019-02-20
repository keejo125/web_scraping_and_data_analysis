# -*- coding: utf-8 -*-
# author：zhengk
import requests
import json
import time
import random
import logging
import csv
import re
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename='maoyan.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' #日志格式
                    )

ua = UserAgent(verify_ssl=False)
count = 1
# 每次抓取评论数，猫眼最大支持30
limit = 30
# 流浪地球
movieId = '248906'
ts = 0
offset = 0


def get_url():
    global offset
    url = 'http://m.maoyan.com/review/v2/comments.json?movieId=' + movieId + '&userId=-1&offset=' + str(
        offset) + '&limit=' + str(limit) + '&ts=' + str(ts) + '&type=3'
    return url


def write_txt(str):
    with open('comment.txt', 'a') as f:
        f.write(str)


def write_csv(datetime, comment):
    with open('comment.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([datetime, comment])


def write_url(str):
    with open('url.txt', 'a') as f:
        f.write(str)


def open_url(url):
    global ua
    try:
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None


def parse_json(data):
    global count
    global offset
    global limit
    global ts
    ts_duration = ts
    res = json.loads(data)
    comments = res['data']['comments']
    for comment in comments:
        comment_time = comment['time']
        if ts == 0:
            ts = comment_time
            ts_duration = comment_time
        if comment_time != ts and ts == ts_duration:
            ts_duration = comment_time
        if comment_time !=ts_duration:
            ts = ts_duration
            offset = 0
            return get_url()
        else:
            content = re.sub("[\r\n|\r|\n|;]", "。", comment['content'].strip()) #comment['content'].strip().replace('\n', '。')
            # content = re.sub("[\s+\.\!\/_,$%^*()+\"\'\?]+|[+——！，。？、~@#￥%……&*（）【】；：]+|\[.+\]|\［.+\］", "", comment['content'].strip())
            logging.info('get comment ' + str(count))
            count += 1
            write_csv(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(comment_time/1000)), content)
            # write_txt(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(comment_time/1000)) + '##' + content + '\n')
    if res['paging']['hasMore']:
        offset += limit
        return get_url()
    else:
        return None


if __name__ == '__main__':
    logging.info('start get comment')
    url = get_url()
    while True:
        try:
            write_url(url + '\n')
            data = open_url(url)
            if data:
                url = parse_json(data)
                if not url:
                    logging.info('end')
                    break
        except Exception as e:
            logging.exception("程序异常")
            time.sleep(random.random() * 3)
