from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import *
from django.db.models import Sum, Count, Value
from django.db.models.functions import Replace  


def index(request):
    product_data = Product.objects.all()
    review_data = Review.objects.all()
    review_avg =  "%.2f" % (Review.objects.count() / Product.objects.count())
    review_rating_sum = Sum(Review.objects.values('review_rating'))
    rating_sum = 0
    for i in Review.objects.values('review_rating'):
        rating_sum += i["review_rating"]

    rating_sum_avg = "%.2f" % (rating_sum / Review.objects.count())

    return render(
        request,
            'common/index.html',
            {   
                'product_data': product_data,
                'review_data': review_data,
                'review_avg' : review_avg,
                'rating_sum_avg' : rating_sum_avg
            }
    )

def price_chart(request):
    labels = []
    data = []

    prd_price = Product.objects.values('prd_price')
    # prd_price = prd_price.replace("원", "")
    # prd_price = prd_price.replace(",", "")
    # prd_price = int(prd_price)

    # Product.objects.update(field=Replace(
    #     'prd_price', Value('string'), Value('int')
    # ))


    queryset = Product.objects.values('prd_id').annotate(price=Sum('prd_price')).order_by('-price')
    for entry in queryset:
        labels.append(entry['prd_id'])
        data.append(entry['price'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
def review_chart(request):
    labels = []
    # 상품명을 라벨로 둔다
    data = []
    # 리뷰수를 보여준다

    queryset = Review.objects.values('prd_id').annotate(review_total=Sum('review_id')).order_by('-review_total')
    
    for entry in queryset:
        labels.append(entry['prd_id'])
        data.append(entry['review_total'])
        # 위에 작성한 annotate (리뷰수 합계)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data
    })

def chart3(request):
    labels = [] # 리뷰 등록날짜
    data = [] # 등록된 리뷰갯수

    queryset = Review.objects.values('review_date').annotate(
        cnt = Count('review_date'),
    )

    for row in queryset:
        labels.append(row['review_date'])
        data.append(row['cnt'])


    print(labels)    
    print(data)    
    return JsonResponse(data={
        'labels': labels,
        'data': data
    })