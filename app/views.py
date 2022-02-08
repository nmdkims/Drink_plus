from django.http import HttpResponse
from django.shortcuts import render
from .models import Img
from test.models import TestModel


# Create your views here.
def new(request):
    if request.method == 'POST':
        img_file = request.FILES['file']
        Img.objects.create(Img=img_file)
        return HttpResponse('업로드 성공', status=200)
    return render(request, 'new.html')


def main(request):
    return render(request, 'main.html')


def search(request):
    if request.method == 'GET':

        query = request.GET['query']
        title = TestModel.objects.filter(title__contains=query)
        category = TestModel.objects.filter(category_name__contains=query)
        selectdrink = title.union(category)

        context = {
            'selectdrink': selectdrink,
            "query": query,
        }

        return render(request, 'search.html', context, )


    elif request.method == 'POST':
        return render(request, 'search.html')



# 검색 후 상세페이지 함수
def description(request,pk):

    selectdrink = TestModel.objects.get(id=pk)
    context = {
        'selectdrink': selectdrink,
    }

    return render(request, 'detail.html', context)
