from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.parse
from urllib.request import Request, urlopen
import time
import math 
import pymysql 
import emoji
from common.models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
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
def apmallupdate(request):     
    driver = wd.Chrome(executable_path='/Users/DaeHyeon/PythonStudy/lecture/chromedriver')

    ########## url과 brand 설정 ##########
    ap_url = 'https://www.amorepacificmall.com'
    brand_name = '이니스프리'

    ########## url 접속 후 brand name 검색 ##########
    driver.get(ap_url)

    driver.find_element_by_class_name('layer_close').click()

    driver.find_element_by_id('query_str').send_keys(brand_name)
    driver.find_element_by_class_name('btn_search').click()
    time.sleep(1)
    driver.find_element_by_css_selector('#ap_container > div > div > div.cont_area.search > div.search_sort > a:nth-child(3)').click()
    time.sleep(1)
    
    obj_id = []
    prd_cell = driver.find_elements_by_class_name('item item-apply') #웹 전체 물품 태그
    print(prd_cell)
    products_url=Product.objects.filter(shop=2) #모든 기존품 url 객체리스트
    last_title=Product.objects.filter(shop=2).last().prd_name_shop#마지막으로 추가된 상품의 title
    
    for prd in prd_cell:  #웹 전체 물품 객체리스트 객체 한개씩 뽑음
        prd_title=prd.find_element_by_class_name('txt_summary ellipsis line2').text #기존물품인지 확인을 위해 title뽑음
        if prd_title==last_title : #기존물품이면 스탑
            break
        obj_id.append(prd.find_element_by_css_selector('a').get_attribute('href')[-5:])   
    obj_id.reverse() # 리버스를 안해주면 신상 of 신상이 마지막에 추가가 안된다.
##########새로상품추가
    print(obj_id)
    k = 1
   
    for i in obj_id:
        ########## 얻은 제품 id로 각 제품 url에 접속 ##########
        driver.get(ap_url + '/kr/ko/product/detail?onlineProdSn=' + i)
        time.sleep(1)
        
        ########## name, price, review count, point ##########
        prd_name = driver.find_element_by_class_name('product_name').text
        prd_price = driver.find_element_by_class_name('product_price').find_element_by_class_name('num').text
        review_count = driver.find_element_by_class_name('review.visibleReview').find_element_by_class_name('txt').text[3:]
        point = driver.find_element_by_css_selector('div > div.detail_head > div > div.product_info > div.purchase_benefit > p').text
        
        shipping_btn = driver.find_element_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(1) > dt > button').click()
        time.sleep(1)
        shipping = driver.find_element_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(1) > dd > div > p').text
        
        purchase_benefit_btn = driver.find_element_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(2) > dt > button').click()
        time.sleep(1)
        purchase_benefits = driver.find_elements_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(2) > dd > div > ul > li')
        benefit_total = ''
        for benefit in purchase_benefits:
            span = benefit.find_element_by_css_selector('span').text
            em = '(' + benefit.find_element_by_css_selector('em').text + ')'
            benefit_total += span + em + " "
    

        ########## 리뷰 200개 이상이면 200으로 표현 ##########
        if ',' in review_count or int(review_count) > 200:
            review_count = '200'
        

        
        ########## 리뷰 200개가 보일 때까지 '더보기' 클릭 ##########
        review_click = driver.find_element_by_css_selector('#ap_container > div > div.detail_body.ui_tab.＠tabs-apply > div.tab_menu > ul > li:nth-child(2) > button').click()
        try:
            if int(review_count) < 200:
                while True:
                    driver.find_element_by_class_name('btn_list_more').click()
                    time.sleep(1)
            else:
                num = 0
                while num < 20:
                    driver.find_element_by_class_name('btn_list_more').click()
                    time.sleep(1)
                    num += 1
        except:
            pass
        shop = Shop.objects.get(shop_id=2)
        Product(
                    shop=shop, ##
                    prd_name_shop=prd_name,  #
                    prd_url=ap_url + '/kr/ko/product/detail?onlineProdSn=' + i, #
                    prd_price=prd_price,  #
                    prd_shipping = shipping, #
                    prd_benefit = benefit_total ).save() #
        
        ########## date, rating, user_id, text ##########
        review_box = driver.find_elements_by_class_name('review_box')
        j = 1
        total_rating = float(0)
        for review in review_box:
            date = review.find_element_by_class_name('rating').find_element_by_class_name('date').text
            rating = review.find_element_by_class_name('rating').find_element_by_css_selector('span:nth-child(1)').get_attribute('class')[-1]
            user_id = review.find_element_by_class_name('name').text
            text = review.find_element_by_class_name('ellipsis.line5').text
            text = emoji.demojize(text)
            total_rating += float(rating)
            j += 1
            Review(
                prd = Product.objects.last(), #
                review_rating = round(float(rating),2)*20 ,#float
                review_text = text,#
                review_date = date,
                review_userid = user_id).save()
       

         
        
        if review_count == '0':
            rating_avg = "0.00"
        else:
            rating_avg = str("%.2f" % (total_rating / int(review_count)))
       

        k += 1
        last=Product.objects.last()
        last.rev_avg=float(rating_avg)*20
        last.rev_cnt=int(review_count)
        last.save()
    ######################원래제품 리뷰 업데이트
    for i in products_url:
        ########## 얻은 제품 id로 각 제품 url에 접속 ##########
        driver.get(ap_url + '/kr/ko/product/detail?onlineProdSn=' + i.prd_url)
        time.sleep(1)
        
        ########## name, price, review count, point ##########
        prd_name = driver.find_element_by_class_name('product_name').text
        prd_price = driver.find_element_by_class_name('product_price').find_element_by_class_name('num').text
        review_count = driver.find_element_by_class_name('review.visibleReview').find_element_by_class_name('txt').text[3:]
        point = driver.find_element_by_css_selector('div > div.detail_head > div > div.product_info > div.purchase_benefit > p').text
        
        shipping_btn = driver.find_element_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(1) > dt > button').click()
        time.sleep(1)
        shipping = driver.find_element_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(1) > dd > div > p').text
        
        purchase_benefit_btn = driver.find_element_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(2) > dt > button').click()
        time.sleep(1)
        purchase_benefits = driver.find_elements_by_css_selector('#ap_container > div > div.detail_head > div > div.product_info > div.purchase_benefit > div > dl:nth-child(2) > dd > div > ul > li')
        benefit_total = ''
        for benefit in purchase_benefits:
            span = benefit.find_element_by_css_selector('span').text
            em = '(' + benefit.find_element_by_css_selector('em').text + ')'
            benefit_total += span + em + " "
    

        ########## 리뷰 200개 이상이면 200으로 표현 ##########
        if ',' in review_count or int(review_count) > 200:
            review_count = '200'
        

        
        ########## 리뷰 200개가 보일 때까지 '더보기' 클릭 ##########
        review_click = driver.find_element_by_css_selector('#ap_container > div > div.detail_body.ui_tab.＠tabs-apply > div.tab_menu > ul > li:nth-child(2) > button').click()
        try:
            if int(review_count) < 200:
                while True:
                    driver.find_element_by_class_name('btn_list_more').click()
                    time.sleep(1)
            else:
                num = 0
                while num < 20:
                    driver.find_element_by_class_name('btn_list_more').click()
                    time.sleep(1)
                    num += 1
        except:
            pass
        shop = Shop.objects.get(shop_id=2)
        Product(
                    shop=shop, ##
                    prd_name_shop=prd_name,  #
                    prd_url=ap_url + '/kr/ko/product/detail?onlineProdSn=' + i, #
                    prd_price=prd_price,  #
                    prd_shipping = shipping, #
                    prd_benefit = benefit_total ).save() #
        
        ########## date, rating, user_id, text ##########
        review_box = driver.find_elements_by_class_name('review_box')
        j = 1
        total_rating = float(0)
        for review in review_box:
            date = review.find_element_by_class_name('rating').find_element_by_class_name('date').text
            rating = review.find_element_by_class_name('rating').find_element_by_css_selector('span:nth-child(1)').get_attribute('class')[-1]
            user_id = review.find_element_by_class_name('name').text
            text = review.find_element_by_class_name('ellipsis.line5').text
            text = emoji.demojize(text)
            total_rating += float(rating)
            j += 1
            Review(
                prd = Product.objects.last(), #
                review_rating = round(float(rating),2)*20 ,#float
                review_text = text,#
                review_date = date,
                review_userid = user_id).save()
       
    

def glowpickupdate(request):       
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







#######gsshop#######
def gsmallupdate(request):
    cursor=None
    #디비연결 
    try : 
        conn = pymysql.connect(
            host='localhost', user = 'root', password ='1234', 
            db = 'cosmetics', charset='utf8')
        cursor = conn.cursor()
    except Exception as e:
        print('db', e)
        
    #드라이버 연결 
    driver = wd.Chrome(executable_path='/Users/DaeHyeon/PythonStudy/lecture/chromedriver')
    url = 'https://with.gsshop.com/shop/search/main.gs?tq=%EC%9D%B4%EB%8B%88%EC%8A%A4%ED%94%84%EB%A6%AC&rq=&cls=&eh=eyJzb3J0VHlwZSI6IkRFRkFVTFQiLCJzZWxlY3RlZCI6Im9wdC1zb3J0In0%3D'

    driver.get(url)
    driver.find_element_by_css_selector('#filter-sort > div > span:nth-child(5) > label').click()


    #각 게시물 정보 가져오기
    posting=0 #게시물 갯수
    endPage=0

    pageCnt = driver.find_element_by_id('prd_cnt_').text
    pageCnt = int(pageCnt[1:4])
    totalPage = math.ceil(pageCnt/60) 

    #메인화면
    links = []
    prd_cell = driver.find_elements_by_class_name('list-item') #웹 전체 물품 태그
    prd_cell2=prd_cell[1:] #웹 전체 물품 객체리스트
    

   
    products_url = Product.objects.filter(shop=4) #모든 기존품 url 객체리스트
    last_title = Product.objects.filter(shop=4).last().prd_name_shop#마지막으로 추가된 상품의 title
    
##########새로상품추가
    time.sleep(3)
    #searchPrdList > section > ul > li:nth-child(34) > a > dl > dd.user-side > button.user-comment
    li_lists = driver.find_elements_by_css_selector('#searchPrdList li')
   
   
    for li_list in li_lists :
        prd_title=li_list.find_element_by_class_name('prd-name').text
        if prd_title==last_title :
            break
        links.append(li_list.find_element_by_css_selector('a').get_attribute('href')) #링크
        posting = posting+1
    links.reverse()
    print('총 게시물수 : ', posting)
    
#상세페이지 1

    scores=[]
    re_dates=[]
    re_cons=[]
    start=0
    end=0

    for i in range(0,len(links)):
        time.sleep(2)
        start = start+1
        print('/////////////////////start', start, '///////////////////////////')
        driver.execute_script('location = "' + links[i] + '"') #상세페이지 접속
        link = links[i]
        time.sleep(3)
        detail = driver.find_element_by_css_selector('.product_detailN_right') #구역지정

        #가격 prices
        price = detail.find_element_by_css_selector('span.price-definition-ins strong').text
        #상품명 de_titles
        de_title = detail.find_element_by_css_selector('.basic_info p').text 
        #찜 de_se
        try :
            de_se = detail.find_element_by_css_selector('#spWishPrdCnt').text
            de_se = int(de_se)
        except Exception as e :
            de_se = int(0)
            print('찜', e)
            
        #카드
        pur1 = detail.find_element_by_css_selector('dl:nth-child(1)>dt.purchase-merit-title').text
        pur1_con = detail.find_element_by_css_selector('dl:nth-child(1) > dd > div.purchase-merit-substance-single').text #물음표 안지워짐
    
        #무이자 구매혜택
        pur2 = detail.find_element_by_css_selector('dl:nth-child(2) .purchase-merit-title').text
        pur2_con = detail.find_element_by_css_selector('dl:nth-child(2) > dd > div.purchase-merit-substance-single>strong').text
    
        #배송정보 배송비 무료배송 
        try :
            pur3 = detail.find_element_by_css_selector('dl:nth-child(3) .purchase-merit-title').text
        except Exception as e :
            pur3 = 'null'
            print('혜택3', e)
        try :
            pur3_con = detail.find_element_by_css_selector('dl:nth-child(3) > dd > div.purchase-merit-substance-single').text
        except:
            pur3_con = 'null'
        
        #상세페이지 3
        driver.find_element_by_css_selector('#ProTab>li:nth-child(2)').click()
        
        #평점 vals 4.8
        time.sleep(4)
        try : 
            val = driver.find_element_by_css_selector('#eval-info > div.eval-score > div > span.gpa > strong').text
            val = float(val)*20
        except Exception as e :
            val = float(0)
            print('평점없음', e)
            
        #평가인원 peson 73 int
        
        try:
            person = driver.find_element_by_css_selector('#eval-info > div.eval-score > div > span.participating-person').text[:-1]
            print("person:::::::::"+person)
            person = int(person)
        except Exception as e :
            person = '0'
            print(e)

        sql = '''INSERT INTO product (shop_id,prd_url, prd_price, prd_name_shop,
                    prd_discount, prd_shipping, prd_benefit, rev_avg, rev_cnt ) 
                    VALUES (%s,%s, %s,%s, %s,%s, %s,%s, %s) '''
 
        cursor.execute(sql, (4,link, price, de_title, pur1_con, pur2_con, pur3_con, val, person ))
        conn.commit()
        prd_id = cursor.lastrowid
        print(prd_id)

        click = int(person)//10
        
        if person==0 :
            scores.append(float(0))
            re_dates.append('null')
            re_cons.append('null')

        #리뷰 내 다음페이지 클릭    
        else : 
            n= int(person)
            for i in range(0, click+1):
                time.sleep(4)
                revs = driver.find_elements_by_css_selector('#reveiw-list > article')
                time.sleep(2)
                for rev in revs :
                    score = rev.find_element_by_css_selector('em').get_attribute('style')[7:-2]
                    score = float(score)
                    scores.append(score)
                    re_date = rev.find_element_by_css_selector('header > div.write-info > span.date').text
                    re_dates.append(re_date)
                    re_con = rev.find_element_by_css_selector('main > p').text
                    re_con = emoji.demojize(re_con)
                    re_cons.append(re_con)
                    n = n - 1

            #n//10 몫이 있으면 다음 페이지가 있는거니까 또는 나머지가 있으면 다음페이지가 있는거니까 
                if n // 10 > 0 or n % 10 > 0:
                    time.sleep(3)
                    driver.find_element_by_css_selector('#revwPagingBtn > button.gui-btn.small.outline.go-next').click()
            
        #테이블 입력
        for i in range(0, len(re_dates)):
            sql = '''INSERT INTO review (review_rating, review_text, review_date, prd_id)
                                    VALUES(%s, %s, %s, %s)'''

            cursor.execute(sql, (scores[i], re_cons[i], re_dates[i], prd_id))
            conn.commit()
        scores =[]
        re_cons = []
        re_dates = []
        end = end+1
        print('/////////////////////end ', end, '///////////////////////////')


    scores=[]
    re_dates=[]
    re_cons=[]
    start=0
    end=0

    for product_url in products_url:

        time.sleep(2)
        start = start+1
        prdurl=product_url.prd_url
        print('/////////////////////start', start, '///////////////////////////')
        driver.execute_script('location = "' + prdurl + '"') #상세페이지 접속
        link = prdurl
        time.sleep(3)
        detail = driver.find_element_by_css_selector('.product_detailN_right') #구역지정

                #평가인원 peson 73 int
        try:
            person = driver.find_element_by_css_selector('#eval-info > div.eval-score > div > span.participating-person').text[:-1]
            print("person:::::::::"+person)
            person = int(person)
        except Exception as e :
            person = '0'
            print(e)

        
        prd_id = cursor.lastrowid
        print(prd_id)

        click = int(person)//10
        
        if person==0 :
            scores.append(float(0))
            re_dates.append('null')
            re_cons.append('null')

        #리뷰 내 다음페이지 클릭    
        else : 
            n= int(person)
            for i in range(0, click+1):
                try:
                    datetemp=driver.find_elements_by_css_selector('#reveiw-list > article:nth-child(1) > header > div > span.date')
                    if datetemp!=time.strftime('%Y.%m.%d', time.localtime(time.time())):
                        break
                except:
                    break
                time.sleep(4)
                revs = driver.find_elements_by_css_selector('#reveiw-list > article')
                time.sleep(2)
                for rev in revs :
                    score = rev.find_element_by_css_selector('em').get_attribute('style')[7:-2]
                    score = float(score)
                    scores.append(score)
                    re_date = rev.find_element_by_css_selector('header > div.write-info > span.date').text
                    re_dates.append(re_date)
                    re_con = rev.find_element_by_css_selector('main > p').text
                    re_con = emoji.demojize(re_con)
                    re_cons.append(re_con)
                    n = n - 1

            #n//10 몫이 있으면 다음 페이지가 있는거니까 또는 나머지가 있으면 다음페이지가 있는거니까 
                if n // 10 > 0 or n % 10 > 0:
                    time.sleep(3)
                    driver.find_element_by_css_selector('#revwPagingBtn > button.gui-btn.small.outline.go-next').click()
            
        #테이블 입력
        for i in range(0, len(re_dates)):
            sql = '''INSERT INTO review (review_rating, review_text, review_date, prd_id)
                                    VALUES(%s, %s, %s, %s)'''

            cursor.execute(sql, (scores[i], re_cons[i], re_dates[i], prd_id))
            conn.commit()
        scores =[]
        re_cons = []
        re_dates = []
        end = end+1
        print('/////////////////////end ', end, '///////////////////////////')
