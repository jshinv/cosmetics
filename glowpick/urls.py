from django.urls import path
from . import views
from django.conf.urls.static
import static from django.conf import settings
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)[
  path('/', views.index),
  path('/update',views.update)+=,
  path('/visible',views.visible)
]