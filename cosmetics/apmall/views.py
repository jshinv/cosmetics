from django.shortcuts import render
from django.http import HttpResponse

        ########## 모듈 import ##########
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as wd
from common.models import Product
from common.models import Shop
from common.models import Review
import time
import emoji
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException


def index(request):
    return render(
        request, 'apmall/index.html', { } )

def crawling(request):

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
    try:
        while True:
            ########## 각 제품의 id get ##########
            prd_cell = driver.find_elements_by_class_name('item.item-apply')
            for prd in prd_cell:
                obj_id.append(prd.find_element_by_css_selector('a').get_attribute('href')[-5:])
            
            
            ########## 다음 페이지로 이동 ##########
            driver.find_element_by_css_selector('span + a').click()
            time.sleep(1)

    ########## 다음 페이지가 없을 때 발생하는 에러 ##########
    except NoSuchElementException as e:
        pass
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
                    
       
   
  
 
   
    
  
    

