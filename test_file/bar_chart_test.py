import matplotlib.pyplot as plt
import numpy as np
import pymysql
import pandas as pd
from matplotlib import font_manager, rc

# 상품에 대한 키워드 box에 들어갈 데이터
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
print(prod_keyword_lst)
#나온 키워드 숫자 리스트화
cnt_keyword_lst = df_keyword_data.head(10)["cnt"].values.tolist()
print(cnt_keyword_lst)


plt.figure(figsize=(3.3,2.3))
y = np.arange(10)

plt.barh(y, cnt_keyword_lst)
plt.yticks(y, prod_keyword_lst)

plt.savefig('bar_chart.jpg')