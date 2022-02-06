from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymysql

driver = webdriver.Chrome(executable_path="../chromedriver.exe")


# 적절한 내용을 입력하여야 작동합니다.
username = ''
password = ''
database_name = ''
host_name = ''



db = pymysql.connect(
    host=host_name,
    port=3306,
    user=username,
    passwd=password,
    db=database_name,
    charset='utf8mb4'
)

cursor = db.cursor()

delete = """
DELETE FROM test;
"""
cursor.execute(delete)

id_num = 0


def main_scraper(category, category_name, id_num):
    i = 0
    driver.get(
        "https://orangebottles.com/")

    time.sleep(5)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    category_tr = soup.select_one(category)
    for tr in category_tr:
        i += 1
        id_num += 1
        try:
            img = tr.select_one('div:nth-child(' + str(i) + ') > div > div.item-thumbs > a > img')['data-original']
            title = tr.select_one('div:nth-child(' + str(i) + ') > div > div.item-detail > a > div > h2').text
            price = tr.select_one('div:nth-child(' + str(i) + ') > div > div.item-detail > a > div > div > p.pay').text
            description = tr.select_one('div:nth-child(' + str(i) + ') > div > div.item-detail > div.item-summary > p '
                                                                    '> span > strong > span').text
        except Exception as e:
            id_num -= 1
            continue

        else:
            print("===================================" + str(i) + "==============================================")
            print('>>>>>>>>>>>>>>>>>>>>' + str(id_num) + '<<<<<<<<<<<<<<<<<')
            print(category_name)
            print(img)
            print(title)
            print(price)
            print(description)

            cursor.execute(
                f"INSERT INTO test VALUES('{id_num}','{category_name}','{img}','{title}','{price.strip()}','{description}')");

            db.commit()
    return id_num


best_wine = '#container_w20210528bf509173d0cea > div.owl-stage-outer > div '
id_num = main_scraper(best_wine, "베스트 와인", id_num)

prize_wine = '#container_w2021092984a7b59f75039 > div.owl-stage-outer > div'
id_num = main_scraper(prize_wine, "상받은 와인", id_num)

vivino_4_wine = '#container_w20210930ce37fd6a8919e > div.owl-stage-outer > div'
id_num = main_scraper(vivino_4_wine, "비비노4.0 이상 대중이 선택한 와인", id_num)

reasonable_price_wine = '#container_w20210930d50feea087638 > div.owl-stage-outer > div '
id_num = main_scraper(reasonable_price_wine, "가성비 추천 와인", id_num)


def sub_scraper(category, category_name, id_num, url, page):
    for p in range(1, page + 1):
        driver.get(
            "https://orangebottles.com/" + str(url) + "/?&page=" + str(p) + "&sort=like")
        print('페이지 전환')
        time.sleep(5)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        category_tr = soup.select_one(category)

        i = 0
        for tr in category_tr:
            i += 1
            if i % 2 == 0:
                try:
                    tr = tr
                    img = tr.select_one('div.shop-item > div.item-wrap > a > img')['src']
                    title = tr.select_one('div.shop-item > div.item-detail > div.item-pay > h2 > a._fade_link').text
                    price = tr.select_one('div.shop-item > div.item-detail > div.item-pay > div.item-pay-detail > '
                                          'p.pay.inline-blocked').text.strip()
                    description = tr.select_one(
                        'div.shop-item > div.item-detail > div.fr-view > p').text.replace("'", "")

                    id_num += 1

                except Exception as e:

                    print(i)
                    print(1000)
                    continue

                else:
                    print("===================================" + str(
                        i) + "==============================================")
                    print(category_name)
                    print(img)
                    print(title)
                    print(price)
                    print(description)
                    print('>>>>>>>>>>>>>>>>>>>>' + str(id_num) + '<<<<<<<<<<<<<<<<<')

                    cursor.execute(
                        f"INSERT INTO test VALUES('{id_num}','{category_name}','{img}','{title}','{price.strip()}','{description}')");

                    db.commit()
            else:
                continue
    return id_num


redwine = '#container_w20210529666f3e476921a'
id_num = sub_scraper(redwine, "레드 와인", id_num, 'redwine', 4)

whitewine = '#container_w202105294a99626bbb2b7'
id_num = sub_scraper(whitewine, "화이트 와인", id_num, 'whitewine', 2)

rosesparkling = '#container_w20210529ef64b0e736f1c'
id_num = sub_scraper(rosesparkling, "로제, 스파클링 와인", id_num, 'rosesparkling', 1)

desert = '#container_w202105292642a56d1aecf'
id_num = sub_scraper(desert, "디저트와인", id_num, '20', 1)

liquor = '#container_w20210529955b74bb3feb8'
id_num = sub_scraper(liquor, "증류주", id_num, 'liquor', 3)

Makgeolli = '#container_w202105292ed77785b254b'
id_num = sub_scraper(Makgeolli, "막걸리, 탁주", id_num, 'Makgeolli', 2)

ricewine = '#container_w20210529e9d2703504f96'
id_num = sub_scraper(ricewine, "청주, 약주", id_num, 'ricewine', 2)

fruitwine = '#container_w20210529fb5665b102dc6'
id_num = sub_scraper(fruitwine, "과실주, 리큐르", id_num, 'fruitwine', 1)

whiskey = '#container_w20211014029472d1f9338'
id_num = sub_scraper(whiskey, "위스키 및 스피릿", id_num, 'whiskey', 2)

beer = '#container_w2021101430db063d5e018'
id_num = sub_scraper(beer, "맥주", id_num, 'beer', 3)

chinaliquor = '#container_w2021101402eccfa6c0d8a'
id_num = sub_scraper(chinaliquor, "백주", id_num, 'chinaliquor', 1)

sake = '#container_w202110148958d638a5da8'
id_num = sub_scraper(sake, "사케", id_num, 'sake', 1)

driver.quit()
