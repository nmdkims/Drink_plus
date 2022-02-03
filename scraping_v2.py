import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import time

import pymysql
import pandas as pd

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get(
    "https://www.visitjeju.net/kr/detail/list?menuId=DOM_000001719001000000&cate1cd=cate0000000005#p1&region2cd"
    "&pageSize=2000&sortListType=reviewcnt&viewType=thumb")
time.sleep(5)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

trs = soup.select_one(
    '#content > div > div.cont_wrap > div.recommend_area > ul')
i = 0
# for tr in trs:
#     i += 1
#     print("===================================" + str(i) + "==============================================")
#     print(tr)


print("=================================================================================")
print(trs)
