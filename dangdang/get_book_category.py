# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import re

url = "http://book.dangdang.com/"
res = requests.get(url)
html = res.content
bsObj = BeautifulSoup(html, 'lxml')
categories = open("dd_category.txt", "w+")

# 获取一级目录
main_categories = bsObj.findAll("a", {"href": re.compile("http\:\/\/category\.dangdang\.com\/cp..\.*")})

for c1 in main_categories:
    c1_href = c1.get("href")
    c1_text = c1.get_text().strip()
    # 获取二级目录
    if len(c1_href) > 15:
        c1_href_prefix = c1_href[:37]
        sub_categories = bsObj.findAll("a", {"href": re.compile(c1_href_prefix+".*")})
        for c2 in sub_categories:
            c2_text = c2.get_text().strip()
            if c2_text != c1_text:
                print(c2_text)
                categories.write(c1_text + ":" + c2_text+"\n")
categories.close()
