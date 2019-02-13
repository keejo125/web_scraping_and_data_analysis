# -*- coding: utf-8 -*-
# author：zhengk
import requests
import json
from time import sleep
import random
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False, verify_ssl=False)
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
    for commnet in comments:
        time = commnet['time']
        if ts == 0:
            ts = time
            ts_duration = time
        if time != ts and ts == ts_duration:
            ts_duration = time
        if time !=ts_duration:
            ts = ts_duration
            offset = 0
            return get_url()
        else:
            content = commnet['content'].strip().replace('\n', '。')
            time = commnet['time']
            print('get comment ' + str(count))
            count += 1
            write_txt(content + '\n')
    if res['paging']['hasMore']:
        offset += limit
        return get_url()
    else:
        return None


if __name__ == '__main__':
    print('start get comment')
    url = get_url()
    while True:
        try:
            write_url(url + '\n')
            data = open_url(url)
            if data:
                url = parse_json(data)
                if not url:
                    print('end')
                    break
        except Exception as e:
            print(e)
            sleep(random.random() * 3)
