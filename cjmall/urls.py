from django.urls import path
from . import views

urlpatterns = [
  path('/', views.index),
  path('/list', views.lists),
  path('/get', views.crawling),
]