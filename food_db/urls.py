from django.urls import path
from . import views

urlpatterns = [
    path('fsearch/', views.food_search, name='fsearch'),
]