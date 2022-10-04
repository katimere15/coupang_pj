import pymysql
import pandas as pd
import numpy as np
import random as rd
from wordcloud import  WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

########################################################################################################################################################################
#가장 많이나온 키워드 10가지
def top_keyword():
    # 상품에 대한 키워드 box에 들어갈 데이터
    conn = pymysql.connect(host = 'localhost',
                    port = 3306,
                    user = 'root',
                    password = '1234',
                    db = 'copang_analysis')
    sql_input = "select keyword,count(keyword) as cnt from keyword_table group by keyword order by cnt desc;"
    df_keyword_data = pd.read_sql_query(sql_input, conn)


    #가장 많이 나온 키워드 10개를 리스트화
    prod_keyword_lst = df_keyword_data.head(10)["keyword"].values.tolist()


    return(prod_keyword_lst)


def keywordinreview(click_keyword):

    conn = pymysql.connect(host = 'localhost',
                    port = 3306,
                    user = 'root',
                    password = '1234',
                    db = 'copang_analysis')
    sql_input = f"select review from review_table where review like ('%{click_keyword}%');"
    df_keyword_in_review_data = pd.read_sql_query(sql_input, conn)

    prod_keyword_in_review_lst = df_keyword_in_review_data["review"].values.tolist()

    rand_review = rd.sample(prod_keyword_in_review_lst,5)


    return(rand_review)
########################################################################################################################################################################
def make_wordcloud():
    conn = pymysql.connect(host = 'localhost',
                port = 3306,
                user = 'root',
                password = '1234',
                db = 'copang_analysis')
    sql_input = "select keyword,count(keyword) as cnt from keyword_table group by keyword having cnt >='3' order by cnt desc;"
    keyword_data = pd.read_sql_query(sql_input, conn)
# 딕셔너리 형태로 데이터를 만들기
    wc_keyword_data = keyword_data.set_index("keyword").to_dict()["cnt"]

    # generate_from_frequencies 함수를 이용해서 워드 클라우드를 출력합니다.
    wc = WordCloud(
        font_path = "C:/Windows/Fonts/NGULIM.TTF",
        background_color='white',
        width=330,
        height=230
    )
    wc_img = wc.generate_from_frequencies(wc_keyword_data)
    wc_img.to_file('./img/wordcloud.jpg')




def make_bar_chart():
    conn = pymysql.connect(host = 'localhost',
                    port = 3306,
                    user = 'root',
                    password = '1234',
                    db = 'copang_analysis')
    sql_input = "select keyword,count(keyword) as cnt from keyword_table group by keyword order by cnt desc;"
    df_keyword_data = pd.read_sql_query(sql_input, conn)

    #한글깨짐 - 폰트 지정코드
    font_path = "C:/Windows/Fonts/NGULIM.TTF"
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)

    #가장 많이 나온 키워드 10개를 리스트화
    prod_keyword_lst = df_keyword_data.head(10)["keyword"].values.tolist()
    #나온 키워드 숫자 리스트화
    cnt_keyword_lst = df_keyword_data.head(10)["cnt"].values.tolist()


    plt.figure(figsize=(3.3,2.3))
    y = np.arange(10)

    plt.barh(y, cnt_keyword_lst)
    plt.yticks(y, prod_keyword_lst)

    plt.savefig('./img/bar_chart.jpg')



########################################################################################################################################################################
def  rating_view(num):
    # five_rating_view
    conn = pymysql.connect(host = 'localhost',
                    port = 3306,
                    user = 'root',
                    password = '1234',
                    db = 'copang_analysis')
    sql_input = f'''select keyword,count(keyword)as count from keyword_table 
        where
        review_num in (select review_num from review_table where review_score = "{num}")
        group by
        keyword
        order by count desc
        limit 10;'''
    df_keyword_data = pd.read_sql_query(sql_input, conn)

    #가장 많이 나온 키워드 10개를 리스트화
    five_rating_keword = df_keyword_data.head(10)["keyword"].values.tolist()

    #입력할 데이터
    return five_rating_keword




########################################################################################################################################################################