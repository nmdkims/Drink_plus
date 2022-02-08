import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Referer': 'https://www.tastings.com/Search-Spirits.aspx',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

driver = webdriver.Chrome(executable_path="chromedriver.exe")


def exception(find, info):
    result = info.select_one(find)
    if result != None:
        result = result.text.strip().replace("'", "")
        return result
    else:
        return ''



def scraping(payload_data, id_num, page):
    response = requests.post('https://www.tastings.com/WebServices/ProcessRequest.asmx/SearchBeer', headers=headers,
                             data=payload_data)
    json_res = json.loads(response.text)
    json_res = json.loads(json_res['d'])

    soup = BeautifulSoup(json_res['HtmlGrid'], 'html.parser')
    category_tr = soup.select('div> div.item ')

    i = 0
    url_base = "https://tastings.com"

    for tr in category_tr:
        i += 1
        try :
            url_detail = str(tr.select_one('div.item > div.img > a ')['href'])
            print("=================================시작=================================")
            # img = url_base + str(tr.select_one('div.item > div.img > a > img')['src'])
            url = url_base + url_detail

            print("url : " + url)
            print("=================================" + str(id_num) + "=================================")
            # ctl00_ContentMain_pnlTastingProducerRow
            driver.get(url)
            print('페이지 전환')
            time.sleep(3)
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')

            print("=================================구조확인=================================")

            # print(soup)

            print("=================================사이트 내용=================================")
            main = soup.select_one('#ctl00_ContentMain_pnlCurrentTopRow')

            # img 값 가져오기
            img = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                  'div.m-review-left-container > '
                                  'div.m-review-left-image-container > img')['src']
            # title 값 가져오기
            brand_name = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                         'div.m-review-middle-container > div.m-review-middle-text-container >'
                                         'h1.m-review-middle-brand-q > #spaSetBrandName ').text.strip().replace("'", "")

            item_name = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                        'div.m-review-middle-container > div.m-review-middle-text-container >'
                                        'h1.m-review-middle-brand-q > #spaBevNameCert ').text.strip().replace("'", "")

            title = brand_name + " [ " + item_name + " ]"

            # category_name 값 가져오기
            category_name = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                            'div.m-review-middle-container > div.m-review-middle-text-container >'
                                            'div.m-review-center-info-text > h3 ').text.lstrip('Category:').strip().replace("'", "")

            # price 값 가져오기
            price = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                    'div.m-review-right-container > div.m-review-medal-container-q >'
                                    '#ctl00_ContentMain_divPrice').text.strip().replace("'", "")
            # description 값 가져오기
            description = main.select_one(
                'div.m-row > div.m-review-testimonials-container> div.m-review-testimonials-text > '
                'span').text.strip().replace("'", "")

            # score 값 가져오기
            score = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                    'div.m-review-right-container > div.m-review-medal-container-q >'
                                    'div.m-review-medal-points-q >span').text.strip().replace("'", "")
            # alcohol 값 가져오기
            alcohol_list = main.select_one('div.m-row > div.m-review-container-q > div.m-container-table > '
                                           'div.m-review-middle-container > div.m-review-middle-text-container >'
                                           'div.m-review-center-info-text')
            ali = 0
            for al in alcohol_list:
                ali += 1
                # print('=======================' + str(ali) + '=================================')
                if ali == 8:
                    alcohol = str(al)
                    if alcohol != None:
                        alcohol = alcohol.lstrip('<div>').lstrip().lstrip('Alcohol:').rstrip('>vid/<').strip().replace("'", "")
                    else:
                        alcohol
                    # print(alcohol)
            print("category_name : " + category_name)
            print("img : " + img)
            print("title : " + title)
            print("price : " + price)
            print("description : " + description)
            print("score : " + score)
            print("alcohol : " + alcohol)

            print("=================================정보 섹터 준비 =================================")
            info = soup.select_one('#ctl00_ContentMain_pnlTastingProducerRow > div.m-row > div.m-container-50-pct > '
                                   'div.m-review-box-left-q > #ctl00_ContentMain_divTastingInfo')

            # info 값 가져오기
            style_info = exception((
                'table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowStyle > '
                'td.m-review-tastings-notes-cell-value'), info)
            aroma_info = exception((
                'table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowAroma > '
                'td.m-review-tastings-notes-cell-value'), info)
            flavor_info = exception((
                'table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowFlavor > '
                'td.m-review-tastings-notes-cell-value'), info)
            smoothness_info = exception(
                ('table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowSmoothness > '
                 'td.m-review-tastings-notes-cell-value'), info)

            finish_info = exception(('table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowFinish > '
                                     'td.m-review-tastings-notes-cell-value'), info)
            enjoy_info = exception((
                'table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowEnjoy > '
                'td.m-review-tastings-notes-cell-value'), info)
            pairing_info = exception((
                'table.m-review-tastings-notes-table-q > tbody > #ctl00_ContentMain_rowPairing > '
                'td.m-review-tastings-notes-cell-value'), info)

            # print(info)
            print("style_info : " + style_info)
            print("aroma_info : " + aroma_info)
            print("flavor_info : " + flavor_info)
            print("finish_info : " + finish_info)
            print("smoothness_info : " + smoothness_info)
            print("enjoy_info : " + enjoy_info)
            print("pairing_info : " + pairing_info)

        except:
            continue

        else:
            id_num += 1
            cursor.execute(
                f"INSERT INTO drink_db VALUES('{id_num}','{category_name}','{img}','{title}','{price.strip()}','{description}','{score}','{alcohol}','{style_info}','{aroma_info}','{flavor_info}','{finish_info}','{smoothness_info}','{enjoy_info}','{pairing_info}','{page}')");

            db.commit()
            print("=================================   완료  =================================")

    return id_num


# 올바른 값을 입력하면 작동 합니다.
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

# 초기화 하는 부분
# delete = """
# DELETE FROM drink_db;
# """
# cursor.execute(delete)

# 양주 관련 김훈희
id_num = 10070
for i in range(9, 101):
    page = i
    data = '{"pQueryString":"PageNo=' + str(
        i) + '&KindWeb=Spirits&View=divGridView&Score=80-100&ABV=0-16&Bitterness=1-9&Price=10-50&Keyword=&KeywordAllAny=Keyword_Any&CountryKind=All&KindGroup=All&SelectAll_Group12=on&SpiritsSearchFilterCatg_12_654=on&SpiritsSearchFilterCatg_12_648=on&SpiritsSearchFilterCatg_12_535=on&SpiritsSearchFilterCatg_12_906=on&SpiritsSearchFilterCatg_12_646=on&SpiritsSearchFilterCatg_12_570=on&SpiritsSearchFilterCatg_12_566=on&SpiritsSearchFilterCatg_12_848=on&SpiritsSearchFilterCatg_12_846=on&SpiritsSearchFilterCatg_12_847=on&SpiritsSearchFilterCatg_12_901=on&SpiritsSearchFilterCatg_12_890=on&SpiritsSearchFilterCatg_12_538=on&SpiritsSearchFilterCatg_12_539=on&SpiritsSearchFilterCatg_12_601=on&SpiritsSearchFilterCatg_12_571=on&SpiritsSearchFilterCatg_12_845=on&SpiritsSearchFilterCatg_12_1082=on&SpiritsSearchFilterCatg_12_568=on&SpiritsSearchFilterCatg_12_876=on&SpiritsSearchFilterCatg_12_602=on&SpiritsSearchFilterCatg_12_541=on&SpiritsSearchFilterCatg_12_536=on&SpiritsSearchFilterCatg_12_604=on&SpiritsSearchFilterCatg_12_864=on&SpiritsSearchFilterCatg_12_887=on&SpiritsSearchFilterCatg_12_898=on&SpiritsSearchFilterCatg_12_542=on&SpiritsSearchFilterCatg_12_513=on&SpiritsSearchFilterCatg_12_647=on&SelectAll_Group10=on&SpiritsSearchFilterCatg_10_445=on&SpiritsSearchFilterCatg_10_438=on&SpiritsSearchFilterCatg_10_568=on&SpiritsSearchFilterCatg_10_440=on&SpiritsSearchFilterCatg_10_441=on&SpiritsSearchFilterCatg_10_442=on&SpiritsSearchFilterCatg_10_443=on&SpiritsSearchFilterCatg_10_711=on&SpiritsSearchFilterCatg_10_444=on&SelectAll_Group11=on&SpiritsSearchFilterCatg_11_685=on&SpiritsSearchFilterCatg_11_716=on&SpiritsSearchFilterCatg_11_717=on&SpiritsSearchFilterCatg_11_715=on&SpiritsSearchFilterCatg_11_714=on&SpiritsSearchFilterCatg_11_540=on&SelectAll_Group6=on&SpiritsSearchFilterCatg_6_624=on&SpiritsSearchFilterCatg_6_625=on&SpiritsSearchFilterCatg_6_855=on&SpiritsSearchFilterCatg_6_706=on&SpiritsSearchFilterCatg_6_191=on&SpiritsSearchFilterCatg_6_190=on&SpiritsSearchFilterCatg_6_731=on&SelectAll_Group9=on&SpiritsSearchFilterCatg_9_721=on&SpiritsSearchFilterCatg_9_171=on&SpiritsSearchFilterCatg_9_193=on&SpiritsSearchFilterCatg_9_514=on&SelectAll_Group2=on&SpiritsSearchFilterCatg_2_633=on&SpiritsSearchFilterCatg_2_228=on&SpiritsSearchFilterCatg_2_842=on&SpiritsSearchFilterCatg_2_677=on&SpiritsSearchFilterCatg_2_229=on&SpiritsSearchFilterCatg_2_230=on&SpiritsSearchFilterCatg_2_231=on&SpiritsSearchFilterCatg_2_232=on&SpiritsSearchFilterCatg_2_659=on&SpiritsSearchFilterCatg_2_233=on&SpiritsSearchFilterCatg_2_234=on&SpiritsSearchFilterCatg_2_843=on&SpiritsSearchFilterCatg_2_839=on&SpiritsSearchFilterCatg_2_235=on&SpiritsSearchFilterCatg_2_800=on&SpiritsSearchFilterCatg_2_853=on&SpiritsSearchFilterCatg_2_1075=on&SpiritsSearchFilterCatg_2_1076=on&SpiritsSearchFilterCatg_2_838=on&SpiritsSearchFilterCatg_2_555=on&SelectAll_Group7=on&SpiritsSearchFilterCatg_7_4=on&SpiritsSearchFilterCatg_7_263=on&SpiritsSearchFilterCatg_7_485=on&SpiritsSearchFilterCatg_7_264=on&SpiritsSearchFilterCatg_7_489=on&SpiritsSearchFilterCatg_7_812=on&SpiritsSearchFilterCatg_7_585=on&SpiritsSearchFilterCatg_7_266=on&SpiritsSearchFilterCatg_7_486=on&SpiritsSearchFilterCatg_7_487=on&SpiritsSearchFilterCatg_7_265=on&SpiritsSearchFilterCatg_7_488=on&SelectAll_Group8=on&SpiritsSearchFilterCatg_8_683=on&SpiritsSearchFilterCatg_8_913=on&SpiritsSearchFilterCatg_8_430=on&SpiritsSearchFilterCatg_8_669=on&SpiritsSearchFilterCatg_8_431=on&SpiritsSearchFilterCatg_8_884=on&SpiritsSearchFilterCatg_8_432=on&SpiritsSearchFilterCatg_8_689=on&SpiritsSearchFilterCatg_8_688=on&SpiritsSearchFilterCatg_8_690=on&SpiritsSearchFilterCatg_8_428=on&SpiritsSearchFilterCatg_8_883=on&SpiritsSearchFilterCatg_8_881=on&SpiritsSearchFilterCatg_8_631=on&SpiritsSearchFilterCatg_8_882=on&SpiritsSearchFilterCatg_8_433=on&SelectAll_Group3=on&SpiritsSearchFilterCatg_3_615=on&SpiritsSearchFilterCatg_3_567=on&SpiritsSearchFilterCatg_3_23=on&SpiritsSearchFilterCatg_3_136=on&SpiritsSearchFilterCatg_3_137=on&SpiritsSearchFilterCatg_3_139=on&SpiritsSearchFilterCatg_3_140=on&SpiritsSearchFilterCatg_3_25=on&SpiritsSearchFilterCatg_3_141=on&SpiritsSearchFilterCatg_3_26=on&SpiritsSearchFilterCatg_3_142=on&SelectAll_Group13=on&SpiritsSearchFilterCatg_13_665=on&SpiritsSearchFilterCatg_13_608=on&SpiritsSearchFilterCatg_13_663=on&SpiritsSearchFilterCatg_13_664=on&SpiritsSearchFilterCatg_13_582=on&SpiritsSearchFilterCatg_13_212=on&SpiritsSearchFilterCatg_13_886=on&SpiritsSearchFilterCatg_13_543=on&SpiritsSearchFilterCatg_13_718=on&SpiritsSearchFilterCatg_13_655=on&SpiritsSearchFilterCatg_13_644=on&SpiritsSearchFilterCatg_13_836=on&SpiritsSearchFilterCatg_13_611=on&SelectAll_Group15=on&SpiritsSearchFilterCatg_15_607=on&SpiritsSearchFilterCatg_15_349=on&SpiritsSearchFilterCatg_15_512=on&SpiritsSearchFilterCatg_15_558=on&SelectAll_Group4=on&SpiritsSearchFilterCatg_4_85=on&SpiritsSearchFilterCatg_4_166=on&SpiritsSearchFilterCatg_4_917=on&SpiritsSearchFilterCatg_4_763=on&SpiritsSearchFilterCatg_4_84=on&SpiritsSearchFilterCatg_4_681=on&SelectAll_Group5=on&SpiritsSearchFilterCatg_5_117=on&SpiritsSearchFilterCatg_5_158=on&SpiritsSearchFilterCatg_5_179=on&SpiritsSearchFilterCatg_5_180=on&SelectAll_Group14=on&SpiritsSearchFilterCatg_14_671=on&SpiritsSearchFilterCatg_14_565=on&SpiritsSearchFilterCatg_14_460=on&SpiritsSearchFilterCatg_14_463=on&SelectAll_Group1=on&SpiritsSearchFilterCatg_1_22=on&SpiritsSearchFilterCatg_1_658=on&SpiritsSearchFilterCatg_1_169=on&SpiritsSearchFilterCatg_1_194=on&SpiritsSearchFilterCatg_1_914=on&SpiritsSearchFilterCatg_1_632=on&SpiritsSearchFilterCatg_1_730=on&SelectAll_Group95=on&SpiritsSearchFilterCatg_95_61=on&SpiritsSearchFilterCatg_95_147=on&SpiritsSearchFilterCatg_95_638=on&SpiritsSearchFilterCatg_95_257=on&SpiritsSearchFilterCatg_95_296=on&SelectAll_Group96=on&SpiritsSearchFilterCatg_96_630=on&SpiritsSearchFilterCatg_96_660=on&SpiritsSearchFilterCatg_96_662=on&SpiritsSearchFilterCatg_96_661=on&SpiritsSearchFilterCatg_96_833=on&SpiritsSearchFilterCatg_96_830=on&SpiritsSearchFilterCatg_96_831=on&SelectAll_Group97=on&SpiritsSearchFilterCatg_97_889=on&SpiritsSearchFilterCatg_97_1088=on&SpiritsSearchFilterCatg_97_637=on&SelectAll_Group101=on&SpiritsSearchFilterCatg_101_869=on&SpiritsSearchFilterCatg_101_868=on&SpiritsSearchFilterCatg_101_874=on&SpiritsSearchFilterCatg_101_866=on&SpiritsSearchFilterCatg_101_871=on&ReviewDate=3"}'
    id_num = scraping(data, id_num, page)

# 와인 관련 양성진
id_num = 20000
for i in range(1, 101):
    page = i
    data = '{"pQueryString":"PageNo=' + str(
        i) + '&KindWeb=Wine&View=divGridView&Score=80-100&ABV=0-16&Bitterness=1-9&Price=10-50&Keyword=&KeywordAllAny=Keyword_Any&CountryKind=All&KindType=All&SelectAll_Red_Varietal=on&WineSearchFilterVarietal_Red_2=on&WineSearchFilterVarietal_Red_3=on&WineSearchFilterVarietal_Red_4=on&WineSearchFilterVarietal_Red_73=on&WineSearchFilterVarietal_Red_5=on&WineSearchFilterVarietal_Red_6=on&WineSearchFilterVarietal_Red_7=on&WineSearchFilterVarietal_Red_8=on&WineSearchFilterVarietal_Red_9=on&WineSearchFilterVarietal_Red_10=on&WineSearchFilterVarietal_Red_11=on&WineSearchFilterVarietal_Red_12=on&WineSearchFilterVarietal_Red_13=on&WineSearchFilterVarietal_Red_70=on&WineSearchFilterVarietal_Red_14=on&WineSearchFilterVarietal_Red_15=on&WineSearchFilterVarietal_Red_102=on&WineSearchFilterVarietal_Red_16=on&WineSearchFilterVarietal_Red_17=on&WineSearchFilterVarietal_Red_18=on&WineSearchFilterVarietal_Red_19=on&WineSearchFilterVarietal_Red_20=on&WineSearchFilterVarietal_Red_22=on&WineSearchFilterVarietal_Red_23=on&WineSearchFilterVarietal_Red_77=on&WineSearchFilterVarietal_Red_24=on&WineSearchFilterVarietal_Red_66=on&WineSearchFilterVarietal_Red_25=on&WineSearchFilterVarietal_Red_26=on&WineSearchFilterVarietal_Red_27=on&WineSearchFilterVarietal_Red_28=on&WineSearchFilterVarietal_Red_71=on&WineSearchFilterVarietal_Red_67=on&WineSearchFilterVarietal_Red_21=on&WineSearchFilterVarietal_Red_29=on&WineSearchFilterVarietal_Red_30=on&WineSearchFilterVarietal_Red_31=on&WineSearchFilterVarietal_Red_32=on&WineSearchFilterVarietal_Red_33=on&WineSearchFilterVarietal_Red_34=on&WineSearchFilterVarietal_Red_76=on&WineSearchFilterVarietal_Red_35=on&WineSearchFilterVarietal_Red_36=on&SelectAll_White_Varietal=on&WineSearchFilterVarietal_White_72=on&WineSearchFilterVarietal_White_38=on&WineSearchFilterVarietal_White_40=on&WineSearchFilterVarietal_White_41=on&WineSearchFilterVarietal_White_42=on&WineSearchFilterVarietal_White_43=on&WineSearchFilterVarietal_White_44=on&WineSearchFilterVarietal_White_45=on&WineSearchFilterVarietal_White_46=on&WineSearchFilterVarietal_White_48=on&WineSearchFilterVarietal_White_65=on&WineSearchFilterVarietal_White_51=on&WineSearchFilterVarietal_White_52=on&WineSearchFilterVarietal_White_53=on&WineSearchFilterVarietal_White_54=on&WineSearchFilterVarietal_White_55=on&WineSearchFilterVarietal_White_56=on&WineSearchFilterVarietal_White_57=on&WineSearchFilterVarietal_White_58=on&WineSearchFilterVarietal_White_69=on&WineSearchFilterVarietal_White_59=on&WineSearchFilterVarietal_White_92=on&WineSearchFilterVarietal_White_61=on&WineSearchFilterVarietal_White_62=on&WineSearchFilterVarietal_White_63=on&WineSearchFilterVarietal_White_64=on&WineSearchFilterVarietal_White_68=on&WineSearchFilterVarietal_White_47=on&WineSearchFilterVarietal_White_49=on&WineSearchFilterVarietal_White_75=on&SelectAll_Rose_Catg=on&WineSearchFilterCatg_Rose_670=on&WineSearchFilterCatg_Rose_1005=on&WineSearchFilterCatg_Rose_1069=on&WineSearchFilterCatg_Rose_697=on&WineSearchFilterCatg_Rose_907=on&WineSearchFilterCatg_Rose_1004=on&WineSearchFilterCatg_Rose_1007=on&WineSearchFilterCatg_Rose_651=on&WineSearchFilterCatg_Rose_1006=on&WineSearchFilterCatg_Rose_384=on&WineSearchFilterCatg_Rose_409=on&WineSearchFilterCatg_Rose_692=on&WineSearchFilterCatg_Rose_426=on&WineSearchFilterCatg_Rose_826=on&WineSearchFilterCatg_Rose_586=on&SelectAll_Sweet_Catg=on&WineSearchFilterCatg_Sweet_27=on&WineSearchFilterCatg_Sweet_44=on&WineSearchFilterCatg_Sweet_81=on&WineSearchFilterCatg_Sweet_161=on&WineSearchFilterCatg_Sweet_206=on&WineSearchFilterCatg_Sweet_224=on&WineSearchFilterCatg_Sweet_285=on&WineSearchFilterCatg_Sweet_334=on&WineSearchFilterCatg_Sweet_373=on&WineSearchFilterCatg_Sweet_723=on&WineSearchFilterCatg_Sweet_478=on&WineSearchFilterCatg_Sweet_150=on&WineSearchFilterCatg_Sweet_494=on&WineSearchFilterCatg_Sweet_510=on&WineSearchFilterCatg_Sweet_849=on&SelectAll_Fruit_Catg=on&WineSearchFilterCatg_Fruit_182=on&SelectAll_Sake_Catg=on&SelectAll_Sparkling_Catg=on&WineSearchFilterCatg_Sparkling_58=on&WineSearchFilterCatg_Sparkling_59=on&WineSearchFilterCatg_Sparkling_88=on&WineSearchFilterCatg_Sparkling_87=on&WineSearchFilterCatg_Sparkling_120=on&WineSearchFilterCatg_Sparkling_122=on&WineSearchFilterCatg_Sparkling_897=on&WineSearchFilterCatg_Sparkling_123=on&WineSearchFilterCatg_Sparkling_124=on&WineSearchFilterCatg_Sparkling_125=on&WineSearchFilterCatg_Sparkling_127=on&WineSearchFilterCatg_Sparkling_997=on&WineSearchFilterCatg_Sparkling_1000=on&WineSearchFilterCatg_Sparkling_149=on&WineSearchFilterCatg_Sparkling_164=on&WineSearchFilterCatg_Sparkling_904=on&WineSearchFilterCatg_Sparkling_177=on&WineSearchFilterCatg_Sparkling_469=on&WineSearchFilterCatg_Sparkling_328=on&WineSearchFilterCatg_Sparkling_332=on&WineSearchFilterCatg_Sparkling_338=on&WineSearchFilterCatg_Sparkling_364=on&WineSearchFilterCatg_Sparkling_390=on&SelectAll_Fortified_Catg=on&WineSearchFilterCatg_Fortified_451=on&WineSearchFilterCatg_Fortified_893=on&WineSearchFilterCatg_Fortified_894=on&WineSearchFilterCatg_Fortified_891=on&WineSearchFilterCatg_Fortified_892=on&WineSearchFilterCatg_Fortified_271=on&WineSearchFilterCatg_Fortified_175=on&WineSearchFilterCatg_Fortified_176=on&WineSearchFilterCatg_Fortified_359=on&WineSearchFilterCatg_Fortified_350=on&WineSearchFilterCatg_Fortified_351=on&WineSearchFilterCatg_Fortified_352=on&WineSearchFilterCatg_Fortified_354=on&WineSearchFilterCatg_Fortified_355=on&WineSearchFilterCatg_Fortified_357=on&WineSearchFilterCatg_Fortified_358=on&WineSearchFilterCatg_Fortified_745=on&WineSearchFilterCatg_Fortified_458=on&WineSearchFilterCatg_Fortified_450=on&WineSearchFilterCatg_Fortified_452=on&WineSearchFilterCatg_Fortified_453=on&WineSearchFilterCatg_Fortified_454=on&WineSearchFilterCatg_Fortified_455=on&WineSearchFilterCatg_Fortified_456=on&WineSearchFilterCatg_Fortified_457=on&WineSearchFilterCatg_Fortified_548=on&SelectAll_Cider_Catg=on&SelectAll_Mead_Catg=on&SelectAll_WineCocktail_Catg=on&WineSearchFilterCatg_WineCocktail_811=on&WineSearchFilterCatg_WineCocktail_820=on&WineSearchFilterCatg_WineCocktail_808=on&WineSearchFilterCatg_WineCocktail_810=on&WineSearchFilterCatg_WineCocktail_809=on&WineSearchFilterCatg_WineCocktail_916=on&SelectAll_FlavoredWine_Catg=on&WineSearchFilterCatg_FlavoredWine_824=on&WineSearchFilterCatg_FlavoredWine_821=on&WineSearchFilterCatg_FlavoredWine_1023=on&WineSearchFilterCatg_FlavoredWine_822=on&SelectAll_Vermouth_Catg=on&WineSearchFilterCatg_Vermouth_829=on&WineSearchFilterCatg_Vermouth_515=on&ReviewDate=1"}'
    id_num = scraping(data, id_num, page)

# 맥주 관련 김시은
id_num = 30000
for i in range(1, 101):
    page = i
    data = '{"pQueryString":"PageNo=' + str(
        i) + '&KindWeb=Beer&View=divGridView&Score=80-100&ABV=0-16&Bitterness=1-9&Price=10-50&Keyword=&KeywordAllAny=Keyword_Any&CountryKind=All&KindGroup=All&SelectAll_Group30=on&BeerSearchFilterCatg_30_17=on&BeerSearchFilterCatg_30_35=on&BeerSearchFilterCatg_30_581=on&BeerSearchFilterCatg_30_20=on&BeerSearchFilterCatg_30_211=on&BeerSearchFilterCatg_30_21=on&BeerSearchFilterCatg_30_54=on&BeerSearchFilterCatg_30_580=on&BeerSearchFilterCatg_30_144=on&BeerSearchFilterCatg_30_674=on&BeerSearchFilterCatg_30_162=on&BeerSearchFilterCatg_30_673=on&BeerSearchFilterCatg_30_86=on&BeerSearchFilterCatg_30_163=on&BeerSearchFilterCatg_30_741=on&BeerSearchFilterCatg_30_207=on&BeerSearchFilterCatg_30_215=on&BeerSearchFilterCatg_30_267=on&BeerSearchFilterCatg_30_825=on&BeerSearchFilterCatg_30_446=on&BeerSearchFilterCatg_30_828=on&BeerSearchFilterCatg_30_606=on&BeerSearchFilterCatg_30_476=on&BeerSearchFilterCatg_30_619=on&BeerSearchFilterCatg_30_556=on&SelectAll_Group102=on&BeerSearchFilterCatg_102_878=on&BeerSearchFilterCatg_102_879=on&BeerSearchFilterCatg_102_986=on&BeerSearchFilterCatg_102_920=on&BeerSearchFilterCatg_102_923=on&SelectAll_Group31=on&BeerSearchFilterCatg_31_16=on&BeerSearchFilterCatg_31_45=on&BeerSearchFilterCatg_31_46=on&BeerSearchFilterCatg_31_48=on&BeerSearchFilterCatg_31_614=on&BeerSearchFilterCatg_31_613=on&BeerSearchFilterCatg_31_50=on&BeerSearchFilterCatg_31_51=on&BeerSearchFilterCatg_31_53=on&BeerSearchFilterCatg_31_174=on&BeerSearchFilterCatg_31_584=on&BeerSearchFilterCatg_31_220=on&BeerSearchFilterCatg_31_719=on&BeerSearchFilterCatg_31_221=on&BeerSearchFilterCatg_31_222=on&BeerSearchFilterCatg_31_223=on&BeerSearchFilterCatg_31_434=on&BeerSearchFilterCatg_31_720=on&BeerSearchFilterCatg_31_1=on&BeerSearchFilterCatg_31_710=on&BeerSearchFilterCatg_31_2=on&BeerSearchFilterCatg_31_3=on&SelectAll_Group32=on&BeerSearchFilterCatg_32_620=on&BeerSearchFilterCatg_32_52=on&BeerSearchFilterCatg_32_746=on&BeerSearchFilterCatg_32_172=on&BeerSearchFilterCatg_32_691=on&BeerSearchFilterCatg_32_532=on&BeerSearchFilterCatg_32_533=on&BeerSearchFilterCatg_32_530=on&BeerSearchFilterCatg_32_531=on&BeerSearchFilterCatg_32_534=on&BeerSearchFilterCatg_32_546=on&SelectAll_Group35=on&BeerSearchFilterCatg_35_802=on&BeerSearchFilterCatg_35_18=on&BeerSearchFilterCatg_35_635=on&BeerSearchFilterCatg_35_33=on&BeerSearchFilterCatg_35_57=on&BeerSearchFilterCatg_35_62=on&BeerSearchFilterCatg_35_148=on&BeerSearchFilterCatg_35_152=on&BeerSearchFilterCatg_35_153=on&BeerSearchFilterCatg_35_160=on&BeerSearchFilterCatg_35_208=on&BeerSearchFilterCatg_35_598=on&BeerSearchFilterCatg_35_252=on&BeerSearchFilterCatg_35_254=on&BeerSearchFilterCatg_35_634=on&BeerSearchFilterCatg_35_1094=on&BeerSearchFilterCatg_35_270=on&BeerSearchFilterCatg_35_321=on&BeerSearchFilterCatg_35_343=on&BeerSearchFilterCatg_35_368=on&BeerSearchFilterCatg_35_622=on&BeerSearchFilterCatg_35_518=on&BeerSearchFilterCatg_35_557=on&SelectAll_Group36=on&BeerSearchFilterCatg_36_600=on&BeerSearchFilterCatg_36_32=on&BeerSearchFilterCatg_36_157=on&BeerSearchFilterCatg_36_760=on&BeerSearchFilterCatg_36_167=on&BeerSearchFilterCatg_36_170=on&BeerSearchFilterCatg_36_641=on&BeerSearchFilterCatg_36_209=on&BeerSearchFilterCatg_36_210=on&BeerSearchFilterCatg_36_279=on&BeerSearchFilterCatg_36_572=on&BeerSearchFilterCatg_36_360=on&BeerSearchFilterCatg_36_640=on&BeerSearchFilterCatg_36_799=on&BeerSearchFilterCatg_36_479=on&SelectAll_Group33=on&BeerSearchFilterCatg_33_36=on&BeerSearchFilterCatg_33_707=on&BeerSearchFilterCatg_33_574=on&BeerSearchFilterCatg_33_564=on&BeerSearchFilterCatg_33_764=on&BeerSearchFilterCatg_33_173=on&BeerSearchFilterCatg_33_178=on&BeerSearchFilterCatg_33_587=on&BeerSearchFilterCatg_33_588=on&BeerSearchFilterCatg_33_200=on&BeerSearchFilterCatg_33_909=on&BeerSearchFilterCatg_33_221=on&BeerSearchFilterCatg_33_223=on&BeerSearchFilterCatg_33_1078=on&BeerSearchFilterCatg_33_276=on&BeerSearchFilterCatg_33_747=on&BeerSearchFilterCatg_33_366=on&BeerSearchFilterCatg_33_626=on&BeerSearchFilterCatg_33_470=on&BeerSearchFilterCatg_33_471=on&BeerSearchFilterCatg_33_589=on&BeerSearchFilterCatg_33_743=on&BeerSearchFilterCatg_33_742=on&BeerSearchFilterCatg_33_629=on&ReviewDate=3"}'
    id_num = scraping(data, id_num, page)

driver.quit()
