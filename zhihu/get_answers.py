# -*- coding: utf-8 -*-
import requests
import json
import csv
from bs4 import BeautifulSoup
from time import sleep
import random
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)

def write_csv(item):
    with open('answer_url_all.csv', 'a', encoding='utf_8_sig', newline='') as f:
        fieldnames = ['is_start', 'is_end', 'previous', 'next', 'totals']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writerow(item)

def get_next_url(data):
    try:
        if not data['paging']['is_start']:
            url = data['paging']['previous']
            write_csv(data['paging'])
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
        print(response)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None


def parse_json(data):
    res = json.loads(data)
    answer = ''
    for ans in res['data']:
        soup = BeautifulSoup(ans['content'], features='html.parser')
        answer = soup.text.strip().replace('\n','。')
        # contents = soup.find_all('p')
        # for content in contents:
        #     if content.text.strip() != '':
        #         answer += content.text.strip()
    write_txt(answer + '\n')
    return get_next_url(res)


def write_txt(str):
    with open('answers_all.txt', 'a') as f:
        f.write(str)


def write_url(str):
    with open('urls.txt', 'a') as f:
        f.write(str)


if __name__ == '__main__':
    count = 1
    print('start get answer')
    url = 'https://www.zhihu.com/api/v4/questions/28997505/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=3&offset=3&sort_by=default'
    while True:
        try:
            data = open_url(url)
            if data:
                url = parse_json(data)
                print('get answer ' + str(count))
                count += 1
                if not url:
                    print('end')
                    break
        except Exception as e:
            print(e)
            time.sleep(random.random()*3)
