from django.shortcuts import render
from django.http import HttpResponse
from common.templates.cjmall.crawling import get_data
from common.models import *

def index(request):
    product_data = Product.objects.all()
    review_data = Review.objects.all()
    review_agv =  Review.objects.count() / Product.objects.count()
    return render(
        request,
            'cjmall/index.html',
            {   'product_data': product_data,
                'review_data': review_data,
                'review_agv' : review_agv
            }
    )

# 차트만드는거 참고 주소 : https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
def pie_chart(request):
    labels = []
    data = []

    queryset = Review.objects.order_by('-review_date')
    
    for rdate in queryset:
        labels.append(rdate.review_date)
        # 라벨에는 리뷰 테이블의 날짜를 찍어줘라
        # data.append(rdate.count(review_id))
        # # 데이타에는 리뷰의 갯수를 찍어줘라

    return render(
        request, 'cjmall/datas.html',
        {
        'labels': labels,
        'data': data
    })


def datas(request):
    # prd_id = request.POST.get('prd_id')
    cj_data = Product.objects.all()
    return render(
        request,
            'cjmall/datas.html',
            {'cj_data': cj_data}
    )

def crawling(request):
    get_data()

