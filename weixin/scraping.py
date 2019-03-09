# -*- coding: utf-8 -*-
# author： zhengk
from selenium import webdriver
import time
import logging
import csv
import random
import json
import os

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename='weixin.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' #日志格式
                    )


def get_articles_list(username, password, account):
    url = "https://mp.weixin.qq.com/"
    chrome_options = webdriver.ChromeOptions()
    # option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    driver.implicitly_wait(60)
    driver.get(url)
    driver.find_element_by_name('account').clear()
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('account').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_class_name('btn_login').click()
    # 手动扫码
    time.sleep(10)
    # 打开素材管理
    driver.find_element_by_link_text('素材管理').click()
    # 点击新建图文素材
    driver.find_element_by_class_name('weui-desktop-btn_primary').click()
    # 新建图文素材 会有新建页面
    all_handles = driver.window_handles
    # 切换到新窗口
    driver.switch_to.window(all_handles[1])
    # 点击插入链接
    driver.find_element_by_id('edui24_body').click()
    # 选择查找文章
    driver.find_element_by_xpath('//*[@id="myform"]/div[3]/div[1]/div/label[2]/span').click()
    # 输入公众号名称
    driver.find_element_by_class_name('js_acc_search_input').send_keys('account')
    # 搜索
    driver.find_element_by_class_name('js_acc_search_btn').click()
    # 选择新世相
    # driver.find_element_by_class_name('search_biz_item').text
    # Out[53]: '订阅号\n新世相 微信号：thefair2'
    driver.find_element_by_class_name('search_biz_item').click()

    # 新建Csv
    f = open('/Users/zhengk/PycharmProjects/web_scraping_and_data_analysis/weixin/articles.csv', 'w')
    writer = csv.writer(f, delimiter=';')

    # 选择结果输出部分
    search_article_result = driver.find_element_by_class_name('search_article_result')

    count = 1
    while True:
        # 获取列表
        temp_list = search_article_result.find_elements_by_class_name('my_link_item')
        logging.info("抓取第" + str(count) + "页")
        for item in temp_list:
            title = item.text.replace('\n', ';')
            logging.info(title)
            # 文章链接
            href = item.find_element_by_tag_name('a').get_attribute('href')
            writer.writerow([title, href])
        try:
            search_article_result.find_element_by_class_name('page_next').click()
            count += 1
            time.sleep(random.randint(20,40))
        except Exception as e:
            logging.warning("获取列表失败")
            logging.exception(e)
            driver.quit()
            return
    return


def get_articles():
    appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local"
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    profile = {
        'printing.print_preview_sticky_settings.appState': json.dumps(appState),
        'savefile.default_directory': './articles'
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)
    chrome_options.add_argument('--kiosk-printing')
    driver = webdriver.Chrome(executable_path='../common/chromedriver', options=chrome_options)
    driver.implicitly_wait(60)
    count = 1
    with open('articles.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for line in spamreader:
            try:
                title = line[0].split(';')[1]
                url = line[1]
                print("下载第" + str(count) + "篇，标题：" + title)
                driver.get(url)
                time.sleep(5)
                # 保存PDF
                temp_title = driver.title
                driver.execute_script('window.print();')
                time.sleep(10)
                os.rename('./articles/' + temp_title + '.pdf', './articles/' + title + '.pdf')
                # 保存txt
                content = driver.find_element_by_id('js_article').text
                with open('./text/' + title + '.txt', 'w') as f:
                    f.write(content)
                count += 1
            except Exception as e:
                logging.exception(e)
    driver.quit()
    return


if __name__ == '__main__':
    username = ''
    password = ''
    account = '新世相'
    try:
        # 获取文章列表
        get_articles_list(username, password, account)
        # 获取文章清单
        get_articles()
    except Exception as e:
        logging.warning("程序异常")
        logging.exception(e)
