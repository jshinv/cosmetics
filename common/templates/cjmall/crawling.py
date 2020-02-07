
# 셀레니움으로 화면을 띄워 정보를 가져온다
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as wd
import re
from common.models import *



def get_data():

    # 크롬 브라우져 사용
    driver = wd.Chrome(executable_path='chromedriver')

    driver.get('http://cjmall.com/')

    driver.find_element_by_css_selector('#srh_keyword').send_keys('이니스프리')
    driver.find_element_by_class_name('btn_srh').click()
    driver.implicitly_wait(5)

    # 1. 전체 상품 개수 확인
    totalCnt = driver.find_element_by_css_selector('#control_listing0 > p > em')
    print(totalCnt.text)
    totalCnt = int(totalCnt.text)

    # 2. 전체 페이지 수를 확인
    totalPage = totalCnt // 48 + 1
    if totalCnt % 48 == 0:
        totalPage -= 1
        
    print(totalPage)

    # 1 페이지로 이동

    cjmall_list_datas = []
    prd_num_datas = []
    prd_num_count = 0
    k = 0

    f = open("prd_num_data_file.txt", 'w')

    import time

    for page in range(1, totalPage + 1):    
    # for page in range(1, 2):  
        # 1페이지 에서 출력되는 상품수 : 48개씩, 보여지는 정보를 가져와 저장해라
        datas = driver.find_elements_by_css_selector('#cont_listing0 > div.listing_result.is_preprefix > ul > li')
        for data in datas:
            driver.implicitly_wait(5)
            title = data.find_element_by_css_selector('a > div > strong').text
            img = data.find_element_by_css_selector('img').get_attribute('src')
            price = data.find_element_by_css_selector('span.info_price > span > ins > span').text
            link = data.find_element_by_css_selector('.is_preprefix > ul > li > a').get_attribute('href')

            link_1 = link[:33]
            prd_num = link[33:41]
            link_2 = link[41:54]
            brand_num = link[54:62] # 브랜드 번호
            link_3 = link[62:]


            link_full = link_1 + prd_num + link_2 + brand_num + link_3
            
            prd_num_datas.append(prd_num)
            
            cjmall_list_datas.append({
                'prd_num' : prd_num
            })

            count = len(cjmall_list_datas)
        
            if prd_num_count == 48:
                driver.find_element_by_css_selector('strong + a').click()
            
            f.write(str(k) + " | " + prd_num + " | " + title + "\n" + link_full + "\n" )
            
            k += 1
        
        time.sleep(0.2)
        
    f.close()

    # 저장한 상품번호를 기준으로 상세페이지를 보여줘라

    cjmall_detail_datas = []
    cjmall_review_datas = []

    p = 0
    fr = open("review_file.txt", 'w')



    for prd_num in prd_num_datas:
        driver.get(link_1 + prd_num + link_2 + brand_num + link_3)
        # driver.navigate().to(link_1 + prd_num + link_2 + brand_num + link_3) 
        time.sleep(0.2)
        
        # 상세페이지 내용을 크롤링 하자
        # prd_info = []

        category = driver.find_element_by_css_selector('#content > div.u_breadcrumbs_wrap > ul').text
        title = driver.find_element_by_class_name('prd_tit').text

        price = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/span/strong').text

        discount_sums = driver.find_elements_by_css_selector('#_cardPromotion > div > div > ul')

        card = ''
        for i in discount_sums:
            discount_sum = i.find_element_by_css_selector('li > a').text
            card += discount_sum + " "

        benefit = driver.find_element_by_css_selector('#content > div.prd_wrap > div.prd_detail_cont > div.prd_info_wrap > div.prd_content_wrap > div.benefit_wrap').text

        cjmall_detail_datas.append({
            'title': title,
            'price': price,
            'category': category,
            'card': card,
            'link_full' : link_full,
            'benefit': benefit
        })
        # 리뷰를 가져온다
        reviews = driver.find_elements_by_css_selector('#_MENTION > div.review_line > ul > li')
        pagination_inner = driver.find_elements_by_css_selector('#_MENTION > div.review_line > div.u_pagination > div')
        reviews_count = 0
        driver.execute_script(
            """
            bs = document.querySelectorAll('.review_line .star_score > .blind');

            for(var i = 0; i < bs.length; i++){
                bs[i].classList.remove('blind')
            }
            """
        )
        try:
            for review in reviews:
                
                star = review.find_element_by_xpath('//*[@id="_MENTION"]/div[3]/ul/li[1]/div[1]/span/span').text
                rating = float(star[0:3])


                try:
                    comment = review.find_element_by_css_selector('#_MENTION > div.review_line > ul > li > div.review_cont > div > p').text
                except:
                    comment = 'null'
                    
                review_info = review.find_element_by_css_selector(
                    '#_MENTION > div.review_line > ul > li > div.review_cont > div > span').text

                writer = review.find_element_by_css_selector(
                    '#_MENTION > div.review_line > ul > li > div.review_cont > div > span > em').text

                date = review_info[-10:]
                
                review_title = prd_num + date
                
                cjmall_review_datas.append({
                    'prd_num' : prd_num,
                    'rating' : rating,
                    'comment' : comment,
                    'writer' : writer,
                    'date' : date,
                    'review_title' : review_title
                })

                
                
                p += 1
                
                print(
                    '리뷰수' + " | " + str(p) + " | " + prd_num + " | " + star + "\n" + comment + " | " + writer + " | " + date + "\n")
                print()

            fr.write(str(p) + " | " + prd_num + " | " + star + "\n" + comment + " | " + writer + " | " + date + "\n" )
            page_move = pagination_inner.find_element_by_css_selector('strong + a').click()
            time.sleep(0.2)
        
        except:
            p = 0
            print(prd_num)
        
    fr.close()  
        
    # driver.close()   

    print(len(cjmall_list_datas))
    print(len(cjmall_detail_datas))


    for cjmall_detail_data in cjmall_detail_datas:
        prd_name_shop = cjmall_detail_data['title']     # 상품명
        prd_price = cjmall_detail_data['price']          # 상품가격
        prd_url = cjmall_detail_data['link_full']        # 상세페이지 링크
        prd_discount = cjmall_detail_data['card']
        prd_benefit = cjmall_detail_data['benefit']


        shop = Shop.objects.get(shop_id=4)
        Product(
            prd_name_shop=prd_name_shop,
            prd_price=prd_price,
            prd_url=prd_url,
            prd_discount=prd_discount,
            prd_benefit=prd_benefit,
        ).save()

    time.sleep(0.2)

    for cjmall_review_data in cjmall_review_datas:
        review_title = cjmall_review_data['review_title']
        review_rating = cjmall_review_data['rating']
        review_text = cjmall_review_data['comment']
        review_userid = cjmall_review_data['writer']
        review_date = cjmall_review_data['date']

        Review(
            review_title=review_title,
            review_rating=review_rating,
            review_text=review_text,
            review_userid=review_userid,
            review_date=review_date,
            ).save()

    time.sleep(0.2)
