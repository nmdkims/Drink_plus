from django.urls import path
from . import views

urlpatterns = [
    path('', views.drink_db_view, name='test'),
]