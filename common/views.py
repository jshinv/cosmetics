from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import *
from django.db.models import Sum

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
    
    queryset = Review.objects.all()

    print(queryset)

    # for entry in queryset:
    #     print(queryset.get(review_date=entry['review_date']).count())

    #     # labels.append(entry['review_date'])
    #     # data.append(entry['review_total'])
    #     # 위에 작성한 annotate (리뷰수 합계)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data

    })