from django.urls import path
from . import views

urlpatterns = [
  path('/', views.index),
  path('/datas', views.pie_chart),
  path('/get', views.crawling),
]