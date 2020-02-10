from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import *
from django.db.models import Sum

def index(request):
    product_data = Product.objects.all()
    review_data = Review.objects.all()
    review_agv =  Review.objects.count() / Product.objects.count()
    return render(
        request,
            'common/index.html',
            {   
                'product_data': product_data,
                'review_data': review_data,
                'review_agv' : review_agv
            }
    )

def price_chart(request):
    labels = []
    data = []

    queryset = Product.objects.values('prd_id').annotate(price=Sum('prd_price')).order_by('-price')
    for entry in queryset:
        labels.append(entry['prd_id'])
        data.append(entry['price'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data
    })

def review_chart(request):
    labels = []
    # 상품명을 라벨로 둔다
    data = []
    # 리뷰수를 보여준다

    queryset = Review.objects.values('prd_id').annotate(review_total=Sum('review_id'))
    for entry in queryset:
        labels.append(entry['prd_id'])
        data.append(entry['review_total'])
        # 위에 작성한 annotate (리뷰수 합계)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data
    })