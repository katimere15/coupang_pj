from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from sqlalchemy import create_engine
from pandas import Series, DataFrame
from datetime import datetime

def num_driver(num):
        
    # # 옵션 생성
    # options = webdriver.ChromeOptions()
    # # 창 숨기는 옵션 추가
    # options.add_argument('headless')
    # driver = webdriver.Chrome('chromedriver',chrome_options=options)
    
    # 크롬 드라이버 실행
    input_num = num.split(" - ")
    driver = webdriver.Chrome('chromedriver')
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
    driver.get(f"https://www.coupang.com/vp/products/{input_num[0]}?itemId={input_num[1]}")
    driver.implicitly_wait(5)

    #크롤링 진행 
    prod_num = crawling(driver)
    return prod_num


def crawling(driver):
    #prod__crawling
    # prod_num 상품번호 (상세 정보-prod_detail-에서 마지막 list 갖고 옴)
    prod_detail = driver.find_elements(By.CSS_SELECTOR,'#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-description > ul > li')
    prod_num = prod_detail[-1].text
    prod_num = prod_num.replace('쿠팡상품번호: ','')
    time.sleep(1)

    # prod_name 상품명
    prod_name = driver.find_element(By.CLASS_NAME, "prod-buy-header__title").text
    time.sleep(1)

    # prod_price 가격
    prod_price = driver.find_element(By.CLASS_NAME, "total-price").text
    prod_price = prod_price.replace('원','')
    time.sleep(1)

    # prod_type 상품 카테고리
    prod_types = driver.find_elements(By.CSS_SELECTOR, '#breadcrumb > li')
    prod_type = prod_types[-1].text
    time.sleep(1)

    # prod_pic 상품 사진 주소
    image = driver.find_element(By.CSS_SELECTOR,'#repImageContainer > div.prod-image__items > div.prod-image__item.prod-image__item--active > i').click()
    time.sleep(1) # Using TIME.SLEEP to make sure the bigger size of picture is fully loaded after click()
    prod_pic = driver.find_element(By.CSS_SELECTOR,'#repImageContainer > img').get_attribute('src')

    # print(prod_num, prod_name, prod_price, prod_type, prod_pic, sep='\n')

    df_prod = pd.DataFrame(columns=["prod_num", "prod_name", "prod_price", "prod_type", "prod_pic", "detail_info"]) # column 생성

    # details 한번에 묶음
    detail_list =[]
    for i in range(len(prod_detail)-1):
        detail_list.append(prod_detail[i].text)

    detail = "/ ".join(detail_list)

    new_list2 = []
    new_list2 = [prod_num, prod_name, prod_price, prod_type, prod_pic, detail]
    df_prod.loc[len(df_prod)] = new_list2

    prod_insert(df_prod)
    
############################################################################################################################################################################################################

    #review crawling
    # Scroll down to 1st div
    first = driver.find_element(By.ID, "btfTab")
    driver.execute_script('arguments[0].scrollIntoView(true);', first)
    time.sleep(1)

    # Click "상품평"
    review = driver.find_element(By.CSS_SELECTOR,"#btfTab > ul.tab-titles > li:nth-child(2)")
    review.click()
    time.sleep(4)

    # Click "베스트순" to sort by 별점 and show 높은별점 first
    order = driver.find_element(By.XPATH,'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[2]/div[1]/button[1]')
    order.click()
    # Then, scroll down a bit more (500 pixel)
    driver.execute_script("window.scrollBy(0, +500);")
    time.sleep(2)

    for a in range(1, 6):
        df_review = pd.DataFrame(columns=["prod_num", "review_user", "review_score","review_buydate", "review_prodtype", "review"])  # column 생성

        driver.find_element(By.CSS_SELECTOR, '#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.sdp-review__article__order.js_reviewArticleOrderContainer.sdp-review__article__order--active > div.sdp-review__article__order__star.js_reviewArticleSearchStarSelectBtn').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, f'#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.sdp-review__article__order.js_reviewArticleOrderContainer.sdp-review__article__order--active > div.sdp-review__article__order__star.js_reviewArticleSearchStarSelectBtn > div.sdp-review__article__order__star__option.js_reviewArticleStarSelectOptionContainer > ul > li:nth-child({a})').click()
        time.sleep(3)


        # page 1 - 10 까지 click해서 넘김
        for x in range(2, 12):  
            xpath = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{x}]'
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(3)

            for j in range(1, 6):
            # total 5 reviews per page
            # save to each parameter and change the types
            # save to the list (new_list)
                rating = driver.find_element(
                By.XPATH, f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article[{j}]/div[1]/div[3]/div[1]/div').get_attribute("data-rating")
                rating = int(rating)

                users = driver.find_element(
                By.XPATH, f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article[{j}]/div[1]/div[2]/span').text
                users = str(users)

                review = driver.find_element(
                By.XPATH, f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article[{j}]/div[4]/div').text
                review = str(review)

                dates = driver.find_element(
                By.XPATH, f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article[{j}]/div[1]/div[3]/div[2]').text
                dates = datetime.strptime(dates, '%Y.%m.%d')

                prodtype = driver.find_element(
                By.XPATH, f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article[{j}]/div[1]/div[5]').text
                prodtype = str(prodtype)

                new_list = []
                new_list = [prod_num, users, rating, dates, prodtype, review]
                df_review.loc[len(df_review)] = new_list

        # db insert
        review_insert(df_review)

        # dataframe 초기화
        del df_review
    
    return prod_num










#prod__table 데이터베이스 insert 함수 
def prod_insert(df_prod):
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="1234",
                               db="copang_analysis"))

    df_prod.to_sql(con=engine, name='prod_table',if_exists='append', index=False)


#review__table 데이터베이스 insert 함수 
def review_insert(df_review):
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="1234",
                               db="copang_analysis"))

    df_review.to_sql(con=engine, name='review_table',if_exists='append', index=False)