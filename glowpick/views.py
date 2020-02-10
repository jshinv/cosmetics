from django.shortcuts import render
from django.http import HttpResponse
from common.models import *
import urllib.parse
from urllib.request import Request, urlopen
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
# import emoji
import datetime
import time
import re
import operator
from matplotlib import pyplot
import numpy




def visible(request):
    product_data = Product.objects.all()
    review_data = Review.objects.all()
    review_agv =  Review.objects.count() // Product.objects.count()

    product_title_list=Product.objects.values('prd_name_shop')
    kewords={}
    for product_title in product_title_list:
        title= re.sub('[0123456789-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]',' ',product_title['prd_name_shop'])
        for word in set(title.split(" ")):
            count=kewords.get(word,0)
            kewords[word]=count+1
    kewords.pop('')
    kewords.pop('-')
    kewords.pop('단종')
    kewords = sorted(kewords.items(), key=lambda x: x[1], reverse=True)

    ranklist=dict()
    for word in kewords:
        objlist=Product.objects.filter(prd_name_shop__contains=word[0])
        word_review=[]
        total_rating=0
        idx=0
        for obj in objlist:
            revlist=Review.objects.filter(prd_id=obj.prd_id)
            for rev in revlist:
                word_review.append(rev.review_text)
                total_rating+=rev.review_rating
                idx+=1
        if idx>100 :
            ranklist[word[0]]=[int(total_rating//idx),total_rating,idx,word_review]

    #sales_rank = sorted(sales_rank.items(), key=lambda x: x[1][0], reverse=True)
    ranklist = sorted(ranklist.items(), key=lambda x: x[1][0], reverse=True)
  
    wordlist=[]
    ratinglist=[]
    reviewlist=[]
    for i in range(10):
        wordlist.append(ranklist[i])
        ratinglist.append(ranklist[i][1][0])
        reviewlist.append(ranklist[i][1][2])
 
    pyplot.rcParams["font.family"] = 'Malgun Gothic'
    pyplot.rcParams["font.size"] = 12
    pyplot.rcParams["figure.figsize"] = (10, 8)
    pyplot.figure()

    x = numpy.arange(len(wordlist))
    pyplot.bar(x-0.0, ratinglist, label='별점', width=0.2, color='#dd0000')
    pyplot.bar(x+0.2, reviewlist, label='리뷰수', width=0.2, color='#ddff00')
    pyplot.xticks(x, wordlist) #좌표에 지절될 라벨 설정

    pyplot.legend() #범주 표시
    pyplot.xlabel('keword') #기준축(x축) 라벨 설정
    pyplot.ylabel('수') #데이터축(y축) 라벨 설정
    pyplot.ylim(0, 150) #데이터축 범위 설정
    pyplot.title('Keyword 별 아몰랑') #그래프 설정

    pyplot.savefig('/Users/DaeHyeon/lastproject/cosmetics/image/temp.png')
    pyplot.close()
    return alert('완료')






            
def index(request):
    product_data = Product.objects.all()
    review_data = Review.objects.all()
    review_agv =  Review.objects.count() // Product.objects.count()

    product_title_list=Product.objects.values('prd_name_shop')
    kewords={}
    for product_title in product_title_list:
        title= re.sub('[0123456789-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]',' ',product_title['prd_name_shop'])
        for word in set(title.split(" ")):
            count=kewords.get(word,0)
            kewords[word]=count+1
    kewords.pop('')
    kewords.pop('-')
    kewords.pop('단종')
    kewords = sorted(kewords.items(), key=lambda x: x[1], reverse=True)

    ranklist=dict()
    for word in kewords:
        objlist=Product.objects.filter(prd_name_shop__contains=word[0])
        word_review=[]
        total_rating=0
        idx=0
        for obj in objlist:
            revlist=Review.objects.filter(prd_id=obj.prd_id)
            for rev in revlist:
                word_review.append(rev.review_text)
                total_rating+=rev.review_rating
                idx+=1
        if idx>100 :
            ranklist[word[0]]=[int(total_rating//idx),total_rating,idx,word_review]

    #sales_rank = sorted(sales_rank.items(), key=lambda x: x[1][0], reverse=True)
    ranklist = sorted(ranklist.items(), key=lambda x: x[1][0], reverse=True)
    topfive=list()
    for i in range(5):
        topfive.append(ranklist[i])
            
    return render(
        request,
            'glowpick/index.html',
            {   'product_data': product_data,
                'review_data': review_data,
                'review_agv' : review_agv,
                'topfive':topfive
            }
    )

# 차트만드는거 참고 주소 : https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
def pie_chart(request):
    labels = []
    data = []

    queryset = Review.objects.order_by('-review_date')[:5]
    
    for date in queryset:
        labels.append(review.review_date)
        # 라벨에는 리뷰 테이블의 날짜를 찍어줘라
        data.append(review.count())
        # 데이타에는 리뷰의 갯수를 찍어줘라

    return render(
        request, 'cjmall/index.html',
        {
        'labels': labels,
        'data': data,
    })


def datas(request):
    # prd_id = request.POST.get('prd_id')
    cj_data = Product.objects.all()
    return render(
        request,
            'cjmall/datas.html',
            {'cj_data': cj_data}
    )



def update(request):       
    driver = wd.Chrome(executable_path='/Users/DaeHyeon/PythonStudy/lecture/chromedriver') #드라이버
    actions=ActionChains(driver)
    driver.get('https://www.glowpick.com/search/result?query=%EC%9D%B4%EB%8B%88%EC%8A%A4%ED%94%84%EB%A6%AC') #ㅜ소
    time.sleep(2)

    pNum=driver.find_element_by_css_selector('#gp-search > div > section.section-result.product > h3').text #전체갯수
    pNum=int(pNum[4:-1]) #전체갯수 숫자로 바꾸기

    driver.find_element_by_css_selector('#gp-search > div > section.section-result.product > h3').click()  #다른 곳 아무데나 클릭
 
    
    obj_id = []
    prd_cell = driver.find_elements_by_class_name('list-item') #웹 전체 물품 태그
    prd_cell2=prd_cell[1:] #웹 전체 물품 객체리스트
    

   
    products_url=Product.objects.filter(shop=5) #모든 기존품 url 객체리스트
    last_title=Product.objects.filter(shop=5).last().prd_name_shop#마지막으로 추가된 상품의 title
    
    for prd in prd_cell2:  #웹 전체 물품 객체리스트 객체 한개씩 뽑음
        prd_title=prd.find_element_by_class_name('name').text #기존물품인지 확인을 위해 title뽑음
        if prd_title==last_title : #기존물품이면 스탑
            break
        obj_id.append(prd.find_element_by_css_selector('div>div>meta').get_attribute('content')[33:]) #기존물품아니면 추가
    obj_id.reverse() # 리버스를 안해주면 신상 of 신상이 마지막에 추가가 안된다.
##########새로상품추가
    for idx in obj_id:

        driver.get('https://www.glowpick.com/product/'+idx)
        time.sleep(1)
        ###########################상품정보#########################
        name_shop=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > h1 > span').text
        desc=driver.find_element_by_class_name('product-detail__description').text
        temp=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__volume_price').text
        temp=temp.split('/')
        price=temp[1]
        avg=float(driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__ratings.ratings > span.ratings__score').text)*20
        cnt=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__ratings.ratings > span.ratings__review_count').text
        cnt=cnt.replace(",", "")
        cnt=int(cnt[1:-1])
        shop = Shop.objects.get(shop_id=5)
    
        driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__volume_price > span').click()
        ###########################스크롤#########################
        while(1):
            last_height=driver.execute_script("return document.querySelectorAll('#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section > ul > li').length")
            actions.send_keys(Keys.END).perform()
            time.sleep(0.5)
            new_height = driver.execute_script("return document.querySelectorAll('#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section > ul > li').length")
            if new_height == last_height:
                break
        
    
        itemlist=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section')
        itemlist=itemlist.find_elements_by_class_name('list-item')

        Product(
            shop=shop,
            prd_name_shop=name_shop,
            prd_url='https://www.glowpick.com/product/'+idx,
            prd_desc=desc,
            prd_price=price,
            rev_avg=avg,
            rev_cnt=len(itemlist),).save()
    
        ###########################리뷰 저장#########################
        emo=0
        for item in itemlist:
            name=item.find_element_by_class_name('user-name').text
            text=item.find_element_by_class_name('review').text
            text=emoji.demojize(text)
            rank=item.find_element_by_css_selector('div > div > p > span.info > span.label > span').get_attribute('class')
            rating=float(0)
            
            if "best" in rank:
                rating=100
            elif "good" in rank:
                rating=80
            elif "soso" in rank:
                rating=60
            elif "bad" in rank:
                rating=40
            elif "worst" in rank:
                rating=20
            try:
                Review(
                    prd = Product.objects.last(),
                    review_rating = rating,
                    review_text = text,
                    review_date = time.strftime('%Y.%m.%d', time.localtime(time.time())),
                    review_userid = name
                ).save()
            except:
                emo+=1
                pass
        last=Product.objects.last()
        last.rev_cnt=last.rev_cnt-emo
        last.save()
        

##########리뷰업데이트
    for product_url in products_url: #객체리스트에서 객체 뽑음
       
        driver.get(product_url.prd_url) #객체에서 url봅아서 들감
        time.sleep(1)

        driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__volume_price > span').click()
        ###########################스크롤:일단 오래걸리니 스크롤은뺀다.#########################
        # while(1):  
        #     last_height=driver.execute_script("return document.querySelectorAll('#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section > ul > li').length")
        #     actions.send_keys(Keys.END).perform()
        #     time.sleep(0.5)
        #     new_height = driver.execute_script("return document.querySelectorAll('#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section > ul > li').length")
        #     if new_height == last_height:
        #         break
        
    
        itemlist=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-bottom > li.section-list-review.side-right > section')
        itemlist=itemlist.find_elements_by_class_name('list-item')
        
        ##평점,갯수 업데이트
        avg=float(driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__ratings.ratings > span.ratings__score').text)*20
        cnt=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__ratings.ratings > span.ratings__review_count').text
        cnt=cnt.replace(",", "")
        cnt=int(cnt[1:-1])
        shop = Shop.objects.get(shop_id=5)
        currentP=Product.objects.get(shop=5,prd_url=product_url.prd_url)#마지막으로 추가된 상품의 title
        currentP.rev_cnt=cnt
        currentP.rev_avg=avg
        currentP.save()
        ###########################리뷰 저장#########################
        emo=0
        for item in itemlist:
            date=item.find_element_by_class_name('date').text
            if '시간' not in date: #하루동안만 가져오기
                break
                
            name=item.find_element_by_class_name('user-name').text
            text=item.find_element_by_class_name('review').text
            text=emoji.demojize(text)
            rank=item.find_element_by_css_selector('div > div > p > span.info > span.label > span').get_attribute('class')
            rating=float(0)
            if "best" in rank:
                rating=100
            elif "good" in rank:
                rating=80
            elif "soso" in rank:
                rating=60
            elif "bad" in rank:
                rating=40
            elif "worst" in rank:
                rating=20
            try:
                Review(
                    prd = Product.objects.last(),
                    review_rating = rating,
                    review_text = text,
                    review_date = time.strftime('%Y.%m.%d', time.localtime(time.time())),
                    review_userid = name
                ).save()
            except:
                emo+=1
                pass
            
    return alert('업데이트 완료')




