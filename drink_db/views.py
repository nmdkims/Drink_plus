from django.shortcuts import render
import pandas as pd
import os
import sys

sys.path.append('/Users/yangseongjin/Desktop/DrinkProject/Drink_plus/test')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from drink_db.models import TestModel
import django

django.setup()


def drink_db_view(request):
    print("실행확인TEST")

    category_wine = TestModel.objects.filter(category_name='베스트 와인')

    category_beer = TestModel.objects.filter(category_name='맥주')

    category_ricewine = TestModel.objects.filter(category_name='청주, 약주')

    category_chinaliquor = TestModel.objects.filter(category_name='백주')

    drink = TestModel.objects.all()
    i = 0
    for dr in category_beer:
        i += 1

        print('=========================================='+str(i)+'============================================')
        print(dr)
        name =dr.title.split(']')[1].split('(')[0]
        print('name:' + name)
        print('=======================================================================================')
        name1 = dr.title.replace('[', '')
        print('name1:' + name1)
        name2 = dr.title.replace('[', '').replace(']', '')
        print('name2:' + name2)
        name3 = dr.title.replace('[', '').replace(']', '').replace('>', '')
        print('name3:' + name3)
        name4 = dr.title.replace('[', '').replace(']', '').replace('>', '').replace('<', '')
        print('name4:' + name4)
        print('==========================================종' + str(i) + '료============================================')



    print(category_wine)
    print("==================================================")
    print(category_beer)
    return render(request, 'home.html', {'category_wine': category_wine, 'category_beer': category_beer,
                                         'category_ricewine': category_ricewine,
                                         'category_chinaliquor': category_chinaliquor})
