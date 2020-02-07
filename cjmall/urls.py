from django.urls import path
from . import views

urlpatterns = [
  path('/', views.index),
  path('/datas', views.datas),
  path('/get', views.crawling),
]