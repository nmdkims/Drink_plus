from django.shortcuts import render
import pandas as pd
import os
import sys

sys.path.append('/Users/yangseongjin/Desktop/DrinkProject/Drink_plus/test')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from .models import TestModel


def test_view(request):
    data = TestModel.objects.values()
    df = pd.DataFrame(data)
    data_title = df[df['item_tags2'] == '#카페']
    title_json = data_title.to_json(orient='split')
    context = {
        'title_json': title_json,
    }
    print(data)
    return render(request, 'main.html', context)
