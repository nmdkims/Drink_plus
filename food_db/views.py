from django.shortcuts import render
from .models import FoodModel
# Create your views here.

def food_search(request):
    if request.method == 'GET':

        query = request.GET['query']
        foodTitle = FoodModel.objects.filter(title__icontains=query)
        food_category = FoodModel.objects.filter(category_name__icontains=query)
        selectfood = foodTitle.union(food_category)

        context = {
            'selectfood': selectfood,
            "query": query,
        }

        return render(request, 'search.html', context)


    elif request.method == 'POST':
        return render(request, 'search.html')

