import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import time

import pymysql
import pandas as pd



host_name = "drinkpluscloud.c2ehucnsk9k8.ap-northeast-2.rds.amazonaws.com"
username = "root"
password = "root1234"
database_name = "drinkplus"

db = pymysql.connect(
    host=host_name,
    port=3306,
    user=username,
    passwd=password,
    db=database_name,
    charset='utf8mb4'
)

# client = MongoClient('mongodb+srv://AKBARI:sparta@cluster0.jujbu.mongodb.net/cluster0?retryWrites=true&w=majority')
# db = client.dbakbari


driver = webdriver.Chrome('/Users/yangseongjin/Downloads/chromedriver')
#driver = webdriver.Chrome(executable_path="chromedriver.exe")

# driver = webdriver.Chrome('D:/7team/Drink_plus/chromedriver')
driver = webdriver.Chrome(executable_path="../chromedriver.exe")
driver.get(
    "https://www.visitjeju.net/kr/detail/list?menuId=DOM_000001719001000000&cate1cd=cate0000000005#p1&region2cd"
    "&pageSize=2000&sortListType=reviewcnt&viewType=thumb")
time.sleep(5)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
# content > div > div.cont_wrap > div.recommend_area > ul > li:nth-child(1) > dl > dt > a > img
# content > div > div.cont_wrap > div.recommend_area > ul > li:nth-child(2) > dl > dt > a > p.s_tit
# react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div._9AhH0
# react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(2) > a > div > div._9AhH0
# react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(2) > a > div > div.KL4Bh > img
# react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(3) > a > div > div.KL4Bh > img

# content > div > div.cont_wrap > div.recommend_area > ul > li:nth-child(1) > dl

trs = soup.select_one(
    '#content > div > div.cont_wrap > div.recommend_area > ul')
print('1')
# db.rest.drop()
# 초기화 하는 법 추가 시킬것
cursor = db.cursor()

delete = """
DELETE FROM test;
"""
cursor.execute(delete)
# db.commit()

# drop = """
# DROP TABLE IF EXISTS test;
# """
# cursor.execute(drop)
# db.commit()
# print('2')
# create = """
# CREATE TABLE test (
#     test_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
#     title CHAR(30) NOT NULL,
#     img CHAR(255) NOT NULL,
#     sub_title CHAR(30) NOT NULL,
#     item_tags1 CHAR(30) NOT NULL,
#     item_tags2 CHAR(30) NOT NULL,
#     item_tags3 CHAR(30) NOT NULL,
#     sub_item_tag1 CHAR(30) NOT NULL,
#     sub_item_tag2 CHAR(30) NOT NULL,
#     sub_item_tag3 CHAR(30) NOT NULL,
#     sub_item_tag4 CHAR(30) NOT NULL,
#     sub_item_tag5 CHAR(30) NOT NULL,
#     PRIMARY KEY(test_id)
# ) DEFAULT CHARSET=utf8 COLLATE=utf8_bin
# """
# cursor.execute(create)
# # db.commit()
# print('3')
# time.sleep(3000)

i = 0
print('4')
for tr in trs:
    img = tr.select_one('li > dl > dt > a > img')['src']
    title = tr.select_one('li > dl > dt > a > p.s_tit').text
    sub_title = tr.select_one('li > dl > dt > a > p.s_theme').text
    item_tags1 = tr.select_one(
        'li > dl > dt > a > p.item_tag.prev > a:nth-child(1)')
    if item_tags1 is None:
        item_tags1 = ''
    else:
        item_tags1 = tr.select_one(
            'li > dl > dt > a > p.item_tag.prev > a:nth-child(1)').text
    item_tags2 = tr.select_one(
        'li > dl > dt > a > p.item_tag.prev > a:nth-child(2)')
    if item_tags2 is None:
        item_tags2 = ''
    else:
        item_tags2 = tr.select_one(
            'li > dl > dt > a > p.item_tag.prev > a:nth-child(2)').text
    item_tags3 = tr.select_one(
        'li > dl > dt > a > p.item_tag.prev > a:nth-child(3)')
    if item_tags3 is None:
        item_tags3 = ''
    else:
        item_tags3 = tr.select_one(
            'li > dl > dt > a > p.item_tag.prev > a:nth-child(3)').text
    sub_item_tag1 = tr.select_one(
        'li > dl > dt > a > p.item_tag.next > a:nth-child(1)')
    if sub_item_tag1 is None:
        sub_itme_tag1 = ''
    else:
        sub_item_tag1 = tr.select_one(
            'li > dl > dt > a > p.item_tag.next > a:nth-child(1)').text
    sub_item_tag2 = tr.select_one(
        'li > dl > dt > a > p.item_tag.next > a:nth-child(2)')
    if sub_item_tag2 is None:
        sub_itme_tag2 = ''
    else:
        sub_item_tag2 = tr.select_one(
            'li > dl > dt > a > p.item_tag.next > a:nth-child(2)').text
    sub_item_tag3 = tr.select_one(
        'li > dl > dt > a > p.item_tag.next > a:nth-child(3)')
    if sub_item_tag3 is None:
        sub_itme_tag3 = ''
    else:
        sub_item_tag3 = tr.select_one(
            'li > dl > dt > a > p.item_tag.next > a:nth-child(3)').text
    sub_item_tag4 = tr.select_one(
        'li > dl > dt > a > p.item_tag.next > a:nth-child(4)')
    if sub_item_tag4 is None:
        sub_itme_tag4 = ''
    else:
        sub_item_tag4 = tr.select_one(
            'li > dl > dt > a > p.item_tag.next > a:nth-child(4)').text
    sub_item_tag5 = tr.select_one(
        'li > dl > dt > a > p.item_tag.next > a:nth-child(5)')
    if sub_item_tag5 is None:
        sub_itme_tag5 = ''
    else:
        sub_item_tag5 = tr.select_one(
            'li > dl > dt > a > p.item_tag.next > a:nth-child(5)').text

    i += 1
    print('5')
    # cursor = db.cursor()

    cursor.execute(
        f"INSERT INTO test VALUES('{i}','{title}','{img}','{sub_title}','{item_tags1}','{item_tags2}','{item_tags3}','{sub_item_tag1}','{sub_item_tag2}','{sub_item_tag3}','{sub_item_tag4}','{sub_item_tag5}')");
    print(i)
    db.commit()


    # sql = 'INSERT INTO dbtest.tweet (img,item_tags1,item_tags2,item_tags3,sub_item_tag1,sub_item_tag2,sub_item_tag3,' \
    #       'sub_item_tag4,sub_item_tag5,sub_title, title ) VALUES (%(img)s, %(item_tags1)s, %(item_tags2)s, ' \
    #       '%(item_tags3)s, %(sub_item_tag1)s, %(sub_item_tag2)s ,%(sub_item_tag3)s ,%(sub_item_tag4)s,' \
    #       '%(sub_item_tag5)s,%(sub_title)s,%(title)s); '
    #
    # doc = {
    #     'img': img,
    #     'item_tags1': item_tags1,
    #     'item_tags2': item_tags2,
    #     'item_tags3': item_tags3,
    #     'sub_item_tag1': sub_item_tag1,
    #     'sub_item_tag2': sub_item_tag2,
    #     'sub_item_tag3': sub_item_tag3,
    #     'sub_item_tag4': sub_item_tag4,
    #     'sub_item_tag5': sub_item_tag5,
    #     'sub_title': sub_title,
    #     'title': title
    # }
    #
    # sql = """
    # INSERT INTO tweet (img,	item_tags1,	item_tags2,	item_tags3,	sub_item_tag1,	sub_item_tag2,	sub_item_tag3,	sub_item_tag4,	sub_item_tag5,	sub_title,	title)
    # VALUES (img,	item_tags1,	item_tags2,	item_tags3,	sub_item_tag1,	sub_item_tag2,	sub_item_tag3,	sub_item_tag4,	sub_item_tag5,	sub_title,	title);
    # """

    # print(sql)

    # SQL 문으로 재구성성
    # db.rest.insert_one(doc)
    # blank = db.rest.find_one
print('완료')
db.close()
driver.quit()
