# -*- coding: utf-8 -*-
import requests
import json
import csv
from bs4 import BeautifulSoup
from time import sleep
import random
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)
count = 1


def write_url_csv(item):
    with open('topic_top_answer_url.csv', 'a', encoding='utf_8_sig', newline='') as f:
        fieldnames = ['is_start', 'is_end', 'previous', 'next', 'totals']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writerow(item)


def write_answer_csv(item):
    with open('topic_top_answer.csv', 'a', encoding='utf_8_sig', newline='') as f:
        fieldnames = ['question', 'answer', 'voteup']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writerow(item)


def get_next_url(data):
    try:
        if not data['paging']['is_end']:
            url = data['paging']['next']
            write_url_csv(data['paging'])
            return url
        else:
            return None
    except Exception as e:
        print(e)
        return None


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
    res = json.loads(data)
    global count
    for ans in res['data']:
        if ans['target']['type'] == 'answer':
            # 获取问题
            question = ans['target']['question']['title']
            soup = BeautifulSoup(ans['target']['content'], features='html.parser')
            # 获取答案
            answer = soup.text.strip().replace('\n','。')
            # 获取点赞数
            voteup = ans['target']['voteup_count']
            write_answer_csv({'question': question,
                              'answer': answer,
                              'voteup': voteup})
            print('get topic answer ' + str(count))
            count += 1
    return get_next_url(res)


if __name__ == '__main__':
    count = 1
    print('start get answer')
    # 讨论
    # url = 'https://www.zhihu.com/api/v4/topics/19552330/feeds/top_activity?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Ccomment_count&offset=5&limit=10'
    # 精华
    url = 'https://www.zhihu.com/api/v4/topics/19552330/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count&limit=10&offset=0'
    while True:
        try:
            data = open_url(url)
            if data:
                url = parse_json(data)
                if not url:
                    print('end')
                    break
        except Exception as e:
            print(e)
            sleep(random.random()*3)
