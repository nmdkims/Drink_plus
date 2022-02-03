"""Drink_plus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
import user.views

# 여기 from app 써있는거는 패키지 다운 받는 건가요? 네 일단 받았습니다 앱 이 views는 왜 에러인가요?

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new', views.new, name="new"),
    path('', include('user.urls')),
    path('', views.main, name='main'),

]
