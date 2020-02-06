# 메인 URLS 입니다. 앱을 새로 생성하면 임폴트 해주세요 

from django.contrib import admin
from django.urls import path, include
from common import views
from cjmall import views
from glowpick import views
from gsshop import views
from apmall import views
from innimall import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('shop/', include('common.urls')),
    path('shop/cjmall', include('cjmall.urls')),
    path('shop/glowpick', include('glowpick.urls')),
    path('shop/gsshop', include('gsshop.urls')),
    path('shop/apmall', include('apmall.urls')),
    path('shop/innimall', include('innimall.urls')),
]
