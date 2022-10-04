import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import re
import numpy as np
from konlpy.tag import Okt


# 불용어 리스트 가져오기
f = open("stopword.txt","r")
stopwords = []
while True:
    line = f.readline().strip()
    if not line: 
        break
    stopwords.append(line)

#리뷰 가져오기
conn = pymysql.connect(host = 'localhost',
                port = 3306,
                user = 'root',
                password = '1234',
                db = 'copang_analysis')
sql_input = f"select review from review_table;"

df_keyword_in_review_data = pd.read_sql_query(sql_input, conn)

prod_review_lst = df_keyword_in_review_data["review"].values.tolist()


#가장 긴 리뷰 
max_len = max(len(review) for review in prod_review_lst)



#모델 가져오기
loaded_model = tf.keras.models.load_model('sentiment_analysis_model.h5')

tokenizer = Tokenizer()


def sentiment_predict(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    okt = Okt()
    new_sentence = okt.morphs(new_sentence)
    new_sentence = [word for word in new_sentence if not word in stopwords]
    #   encoded = tokenizer.texts_to_sequences(new_sentence)
    encoded = tokenizer.texts_to_sequences([new_sentence])
    pad_new = pad_sequences(encoded, maxlen = max_len)
    score = loaded_model.predict(pad_new)
    print(score)
    if(score > 0.5):
        print("긍정 리뷰입니다.")
    else:
        print("부정 리뷰입니다.")

    # if(score > 0.5):
    #     print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    # else:
    #     print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))


sentiment_predict(''' 크기가 이렇게 작았던가?
 아님 내 눈이 이상한건가...
 간만에 마주한 동원참치에 대한 나의 생각이다.
 맛은 변함없다만 크기는 실망임. ''')