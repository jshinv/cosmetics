# 셀레니움으로 화면을 띄워 정보를 가져온다
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as wd
import re

# 크롬 브라우져 사용
driver = wd.Chrome(executable_path='chromedriver')

driver.get('http://cjmall.com/')

driver.find_element_by_css_selector('#srh_keyword').send_keys('이니스프리')
driver.find_element_by_class_name('btn_srh').click()
driver.implicitly_wait(5)

# 1. 전체 상품 개수 확인
totalCnt = driver.find_element_by_css_selector('#control_listing0 > p > em')
# print(totalCnt.text)
totalCnt = int(totalCnt.text)

# 2. 전체 페이지 수를 확인
totalPage = totalCnt // 48 + 1
if totalCnt % 48 == 0:
    totalPage -= 1
    
# print(totalPage)

    
# 1 페이지로 이동

cjmall_data_list = []
for page in range(1, totalPage + 1):
# for page in range(1, 3):
    
    # 1페이지 에서 출력되는 상품수 : 48개씩, 보여지는 정보를 가져와 저장해라
    datas = driver.find_elements_by_css_selector('#cont_listing0 > div.listing_result.is_preprefix > ul > li')
    #print(datas)
    for data in datas:
        driver.implicitly_wait(5)
        title = data.find_element_by_css_selector('a > div > strong').text
        img = data.find_element_by_css_selector('img').get_attribute('src')
        price = data.find_element_by_css_selector('span.info_price > span > ins > span').text
        link = data.find_element_by_css_selector('.is_preprefix > ul > li > a').get_attribute('href')

        link_1 = link[:33]
        prd_num = '57215631' # 상품번호
        link_2 = link[41:54]
        brand_num = link[54:62] # 브랜드 번호
        link_3 = link[62:]

        link_full = link_1 + prd_num + link_2 + brand_num + link_3

        cjmall_data_list.append({
            'title': title,
            'price': price,
            'img': img,
            'link' : link,
            'prd_num' : prd_num,
            'link_2' : link_2,
            'brand_num' : brand_num,
            'link_3' : link_3
        })
        # print(cjmall_data_list)
        count = len(cjmall_data_list)
        
    driver.find_element_by_css_selector('strong + a').click()
    driver.implicitly_wait(5)
            
# print(cjmall_data_list)

# print(count)

# driver.close()