from django.http import HttpResponse
from django.shortcuts import render
from .models import Img

# Create your views here.
def new(request):
    if request.method == 'POST':
        img_file = request.FILES['file']
        Img.objects.create(Img=img_file)
        return HttpResponse('업로드 성공', status=200)
    return render(request, 'new.html')


def main(request):
    return render(request, 'main.html')