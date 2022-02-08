from django.shortcuts import render
import pandas as pd
import os
import sys

sys.path.append('/Users/yangseongjin/Desktop/DrinkProject/Drink_plus/test')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from test.models import TestModel
import django

django.setup()


def test_view(request):
    print("실행확인TEST")

    category_wine = TestModel.objects.filter(category_name='베스트 와인')

    category_beer = TestModel.objects.filter(category_name='맥주')

    category_ricewine = TestModel.objects.filter(category_name='청주, 약주')

    category_chinaliquor = TestModel.objects.filter(category_name='백주')

    category_rum= TestModel.objects.filter(category_name__icontains='Rum')

    # drink = TestModel.objects.all()
    i = 0
    for dr in category_beer:
          i += 1

          print(dr)
          name =dr.title.split(']')[1].split('(')[0]
          print(name)


    # print(category_wine)
    # print("==================================================")
    # print(category_beer)
    return render(request, 'home.html', {'category_wine': category_wine, 'category_beer': category_beer,
                                         'category_ricewine': category_ricewine,
                                         'category_rum': category_rum,
                                         'category_chinaliquor': category_chinaliquor})



