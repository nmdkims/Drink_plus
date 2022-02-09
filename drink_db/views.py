from django.shortcuts import render
import pandas as pd
import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append('/Users/yangseongjin/Desktop/DrinkProject/Drink_plus/test')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from drink_db.models import DrinkModel

import django

django.setup()




def drink_db_view(request):
    print("drink_db_view 실행확인")

    user = request.user.is_authenticated
    if user:
        ratings = pd.read_csv('./static/model/drink_ratings.csv')
        drinks = pd.read_csv('./static/model/drinks.csv', encoding='cp949')

        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 300)

        drink_ratings = pd.merge(ratings, drinks, on='drinkid')
        # print(drink_ratings)

        # user별로 영화에 부여한 rating 값을 볼 수 있도록 pivot table 사용
        title_user = drink_ratings.pivot_table('score_x', index='userId', columns='title')

        # 평점을 부여안한 영화는 그냥 0이라고 부여
        title_user = title_user.fillna(0)
        # print(title_user)

        user_based_collab = cosine_similarity(title_user, title_user)
        # print(user_based_collab)

        user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
        # print(user_based_collab)

        # 접속한 유저의 아이디를 받아옴
        id = request.user.id

        # 4번 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 10개만 뽑음
        # print(user_based_collab[id].sort_values(ascending=False)[:10])

        # 4번 유저와 가장 비슷한 266번 유저를 뽑고,
        user = user_based_collab[id].sort_values(ascending=False)[:10].index[1]
        # 266번 유저가 좋아했던 영화를 평점 내림차순으로 출력
        category_recommend = title_user.query(f"userId == {user}").sort_values(ascending=False, by=user, axis=1)

        category_recommend_list = []

        for i, cate in enumerate(category_recommend):
            if i < 10:
                category_recommend_list.append(cate)
            else:
                break

        final_recommend_list = []
        for cate_search in category_recommend_list:
            temp = DrinkModel.objects.filter(title=str(cate_search).lstrip('/'))[0]
            final_recommend_list.append(temp)

        # print(final_recommend_list[0])
        # print(final_recommend_list[0][0])
        # print(final_recommend_list[0][0].title)
        # print(type(final_recommend_list))

        # for cate in category_recommend:
        #     print(cate)
        #     print("========================================================================")

        category_wine = DrinkModel.objects.filter(category_name='베스트 와인')

        category_beer = DrinkModel.objects.filter(category_name='맥주')

        category_ricewine = DrinkModel.objects.filter(category_name='청주, 약주')

        category_chinaliquor = DrinkModel.objects.filter(category_name='백주')

        category_rum = DrinkModel.objects.filter(category_name__icontains='Rum')

        return render(request, 'home.html', {'category_wine': category_wine, 'category_recommend': final_recommend_list,
                                             'category_ricewine': category_ricewine, 'category_beer': category_beer,
                                             'category_rum': category_rum,
                                             'category_chinaliquor': category_chinaliquor})


        # return render(request, 'home.html', {'category_main': category_main, 'category_recommend': category_recommend,
        #                                      'category_recommend2': category_recommend2,
        #                                      'category_random': category_random})

    else:

        category_wine = DrinkModel.objects.filter(category_name='베스트 와인')

        category_beer = DrinkModel.objects.filter(category_name='맥주')


        category_ricewine = DrinkModel.objects.filter(category_name='청주, 약주')

        category_chinaliquor = DrinkModel.objects.filter(category_name='백주')

        category_rum = DrinkModel.objects.filter(category_name__icontains='Rum')

        return render(request, 'home.html', {'category_wine': category_wine, 'category_beer': category_beer,
                                             'category_ricewine': category_ricewine,
                                             'category_rum': category_rum,
                                             'category_chinaliquor': category_chinaliquor})

    # drink = DrinkModel.objects.all()
    # i = 0
    # for dr in category_beer:
    #     i += 1
    #
    #     print('=========================================='+str(i)+'============================================')
    #     print(dr)
    #     name =dr.title.split(']')[1].split('(')[0]
    #     print('name:' + name)
    #     print('=======================================================================================')
    #     name1 = dr.title.replace('[', '')
    #     print('name1:' + name1)
    #     name2 = dr.title.replace('[', '').replace(']', '')
    #     print('name2:' + name2)
    #     name3 = dr.title.replace('[', '').replace(']', '').replace('>', '')
    #     print('name3:' + name3)
    #     name4 = dr.title.replace('[', '').replace(']', '').replace('>', '').replace('<', '')
    #     print('name4:' + name4)
    #     print('==========================================종' + str(i) + '료============================================')
    #
    #
    #
    # print(category_wine)
    # print("==================================================")
    # print(category_beer)

