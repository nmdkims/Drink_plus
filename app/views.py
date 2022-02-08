from django.http import HttpResponse
from django.shortcuts import render
from .models import Img
from drink_db.models import DrinkModel


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
        title = DrinkModel.objects.filter(title__icontains=query)
        category = DrinkModel.objects.filter(category_name__icontains=query)
        selectdrink = title.union(category)

        context = {
            'selectdrink': selectdrink,
            "query": query,
        }

        return render(request, 'search.html', context, )


    elif request.method == 'POST':
        return render(request, 'search.html')



