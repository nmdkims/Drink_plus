# from django.http import HttpResponse
# from django.shortcuts import render
# from .models import FoodModel
# # Create your views here.
#
# def foodsearch(request):
#     if request.method == 'GET':
#         query = request.GET['query']
#         title = FoodModel.objects.filter(title__icontains=query)
#         category = FoodModel.objects.filter(category_name__icontains=query)
#         selectfood = title.union(category)
#
#         context = {
#             "selectfood": selectfood,
#             "query": query,
#         }
#
#         return render(request, '../templates/search.html', context,)
#
#
#     elif request.method == 'POST':
#         return render(request, 'search.html')
#
