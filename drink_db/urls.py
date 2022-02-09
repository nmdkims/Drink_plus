from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.drink_db_view, name='drink_db_view'),
    # path('', include('user.urls')),
]