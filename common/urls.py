from django.urls import path
from . import views

urlpatterns = [
  path('/', views.index),
  path('/price-chart/', views.price_chart, name = 'price-chart'),
  path('/review_chart/', views.review_chart, name = 'review-chart'),
  path('/chart3/', views.chart3, name = 'chart3'),
]