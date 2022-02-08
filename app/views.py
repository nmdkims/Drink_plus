from django.http import HttpResponse
from django.shortcuts import render
from .models import Img
from drink_db.models import DrinkModel
from food_db.models import FoodModel
from django.core.paginator import Paginator

# Create your views here.
def new(request):
    if request.method == 'POST':
        img_file = request.FILES['file']
        Img.objects.create(Img=img_file)
        return HttpResponse('업로드 성공', status=200)
    return render(request, 'new.html')


def main(request):
    return render(request, 'main.html')

#주류와 음식 검색
def search(request):
    if request.method == 'GET':

        query = request.GET['query']
        title = DrinkModel.objects.filter(title__icontains=query)
        category = DrinkModel.objects.filter(category_name__icontains=query)
        foodtitle = FoodModel.objects.filter(title__icontains=query)
        foodcategory = FoodModel.objects.filter(category_name__icontains=query)
        selectfood = foodtitle.union(foodcategory)
        selectdrink = title.union(category)

        context = {
            'selectdrink': selectdrink,
            'selectfood':selectfood,
            "query": query,
        }

        return render(request, 'search.html', context, )


    elif request.method == 'POST':
        return render(request, 'search.html')

#페이지수 제한하는 함수

def question_list(request):
  Drinks = DrinkModel.objects.order_by('id') # DrinkModel 모델 데이터를 아이디값으로 정렬한다.
  # Paging 기능 구현하기
  page = request.GET.get('page', '1') # GET 방식 요청 URL에서 page값을 가져올 때 사용(?page=1). page 파라미터가 없는 URL을 위해 기본값으로 1을 지정한 것
  paginator = Paginator(Drinks, 6) # Paginator 클래스는 questions를 페이징 객체 paginator로 변환. 페이지당 5개씩 보여주기
  page_obj = paginator.get_page(page) # page_obj 객체에는 여러 속성이 존재
  context = { 'Drinks_list' : page_obj } # page_obj를 question_list에 저장한다.
  return render(request, 'search.html', context)

# 검색 후 상세페이지 함수
def description(request,pk):

    selectdrink = DrinkModel.objects.get(id=pk)
    food=FoodModel.objects.order_by()[:3]
    context = {
        'selectdrink': selectdrink,
        'food':food
    }

    return render(request, 'detail.html', context)

# def foodsearch(request):
#     if request.method == 'GET':
#         foodquery = request.GET['query']
#         foodtitle = FoodModel.objects.filter(title__icontains=foodquery)
#         foodcategory = FoodModel.objects.filter(category_name__icontains=foodquery)
#         selectfood = foodtitle.union(foodcategory)
#
#         context = {
#             "selectfood": selectfood,
#             "foodquery": foodquery,
#         }
#
#         return render(request, '../templates/search.html', context,)
#
#
#     elif request.method == 'POST':
#         return render(request, 'search.html')

