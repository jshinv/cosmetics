def crawling(request): 
    driver = wd.Chrome(executable_path='/Users/DaeHyeon/PythonStudy/lecture/chromedriver') #드라이버
    actions=ActionChains(driver)
    driver.get('https://www.glowpick.com/search/result?query=%EC%9D%B4%EB%8B%88%EC%8A%A4%ED%94%84%EB%A6%AC') #ㅜ소
    time.sleep(2)

    pNum=driver.find_element_by_css_selector('#gp-search > div > section.section-result.product > h3').text #전체갯수
    pNum=int(pNum[4:-1]) #전체갯수 숫자로 바꾸기

    driver.find_element_by_css_selector('#gp-search > div > section.section-result.product > h3').click()  #다른 곳 아무데나 클릭

    while(1):
            last_height=driver.execute_script("return document.querySelectorAll('#gp-search > div > section.section-result.product > div > ul > li').length")
            actions.send_keys(Keys.END).perform()
            time.sleep(0.5)
            new_height = driver.execute_script("return document.querySelectorAll('#gp-search > div > section.section-result.product > div > ul > li').length")
            if new_height == last_height:
                break

    obj_id = []
    prd_cell = driver.find_elements_by_class_name('list-item')
    prd_cell2=prd_cell[1:]
    for prd in prd_cell2:
        obj_id.append(prd.find_element_by_css_selector('div>div>meta').get_attribute('content')[33:])
        


    #p=None
    for idx in obj_id:
        driver.get('https://www.glowpick.com/product/'+idx)
        
        ###########################상품정보#########################
        name_shop=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > h1 > span').text
        desc=driver.find_element_by_class_name('product-detail__description').text
        temp=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__volume_price').text
        temp=temp.split('/')
        price=temp[1]
        avg=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__ratings.ratings > span.ratings__score').text
        cnt=driver.find_element_by_css_selector('#gp-product-detail > div > ul.section-list-wrap.side-top > li.section-list-info.side-right > div > section.product-main-info > div.product-main-info__data_wrapper > div.product-main-info__ratings.ratings > span.ratings__review_count').text
        cnt=cnt.replace(",", "")
        cnt=int(cnt[1:-1])*20
        shop = Shop.objects.get(shop_id=5)
        p= Product(
                    shop=shop,
                    prd_name_shop=name_shop,
                    prd_url='https://www.glowpick.com/product/'+idx,
                    prd_desc=desc,
                    prd_price=price,
                    rev_avg=avg,
                    rev_cnt=cnt,).save()
        time.sleep(1)
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
        ###########################리뷰 저장#########################

        for item in itemlist:

            name=item.find_element_by_class_name('user-name').text
            text=item.find_element_by_class_name('review').text
            text=emoji.demojize(text)
            rank=item.find_element_by_css_selector('div > div > p > span.info > span.label > span').get_attribute('class')
            rating=0
            
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
            Review(
                prd = Product.objects.last(),
                review_rating = rating,
                review_text = text,
                review_date = time.strftime('%Y-%m-%d', time.localtime(time.time())),
                review_user_id = name
            ).save()