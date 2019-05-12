# -*- coding: utf-8 -*-
# author：zhengk

import requests
import json
import csv
import time


def update_url(last_comment_id):
    global content_id
    url = 'https://sns-comment.iqiyi.com/v3/comment/get_comments.action?' \
          'content_id=' + content_id + \
          '&types=time&' \
          'last_id=' + last_comment_id + \
          '&business_type=17&agent_type=119&agent_version=9.9.0&authcookie='
    return url


if __name__ == '__main__':
    content_id = '2400411900'
    init_url = 'https://sns-comment.iqiyi.com/v3/comment/get_comments.action?' \
               'content_id=' + content_id + \
               '&types=hot%2Ctime&business_type=17&agent_type=119&agent_version=9.9.0&authcookie='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    res = requests.get(url=init_url, headers=headers)
    # 初始化csvwriter
    f = open('comments.csv', 'w+', newline='')
    writer = csv.writer(f, delimiter=';')

    count = 0

    while res.status_code == 200:
        data = json.loads(res.content)
        last_comment_id = ''
        for comment in data['data']['comments']:
            c_content = comment['content'].strip().replace('\n',';')
            c_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(comment['addTime']))
            c_nickname = comment['userInfo']['uname']
            c_gender = comment['userInfo']['gender']
            writer.writerow([c_time, c_nickname, c_gender, c_content])
            last_comment_id = comment['id']
            count += 1
            print('获取第' + str(count) + '条评论：' + c_content)
        url = update_url(last_comment_id)
        if data['data']['remaining'] == 1:
            res = requests.get(url, headers=headers)
        else:
            break
    print('抓取结束')
    f.close()