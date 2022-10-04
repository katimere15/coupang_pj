import pandas as pd
import pymysql
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine


def keyword__analysis():
    keyword_lst=[]
    conn = pymysql.connect(host = 'localhost',
                        port = 3306,
                        user = 'root',
                        password = '1234',
                        db = 'copang_analysis')
    sql_input = "SELECT review_num,review FROM review_table"

    sql_input2 = "SELECT DISTINCT review_num FROM keyword_table;"

    df_review_data = pd.read_sql_query(sql_input, conn)
    df_keyword_data = pd.read_sql_query(sql_input2, conn)
    #리뷰 리스트화
    review_num_lst = df_review_data["review_num"].values.tolist()
    review_list = df_review_data["review"].values.tolist()
    db_keyword_list = df_keyword_data["review_num"].values.tolist()



    for i in review_num_lst:
        if i not in db_keyword_list:
            #토큰화 및 키워드 추출
            for review in review_list:
                try:
                    okt = Okt()

                    tokenized_doc = okt.pos(review)
                    tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun'])


                    n_gram_range = (1, 1)

                    count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
                    candidates = count.get_feature_names_out()


                    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
                    doc_embedding = model.encode([review])
                    candidate_embeddings = model.encode(candidates)



                    #키워드 추출 함수
                    def max_sum_sim(doc_embedding, candidate_embeddings, words, top_n, nr_candidates):

                        # 문서와 각 키워드들 간의 유사도
                        distances = cosine_similarity(doc_embedding, candidate_embeddings)

                        # 각 키워드들 간의 유사도
                        distances_candidates = cosine_similarity(candidate_embeddings, 
                                                                candidate_embeddings)

                        # 코사인 유사도에 기반하여 키워드들 중 상위 top_n개의 단어를 pick.
                        words_idx = list(distances.argsort()[0][-nr_candidates:])
                        words_vals = [candidates[index] for index in words_idx]
                        distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

                        # 각 키워드들 중에서 가장 덜 유사한 키워드들간의 조합을 계산
                        min_sim = np.inf
                        candidate = None
                        for combination in itertools.combinations(range(len(words_idx)), top_n):
                            sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
                            if sim < min_sim:
                                candidate = combination
                                min_sim = sim
                        return [words_vals[idx] for idx in candidate]

                    try:
                        
                        keyword_lst.append(max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n=5, nr_candidates=10))

                    except TypeError:
                        print("review데이터가 부족합니다. pass 합니다.")

                except ValueError:
                    print("review가 공백입니다. pass 합니다.")

            #review keyword pandas save
            df_keyword = pd.DataFrame(columns=["review_num", "keyword"])  # column 생성
            for num in range(len(keyword_lst)):
                for num2 in range(len(keyword_lst[num])):
                    df = [review_num_lst[num],keyword_lst[num][num2]]
                    df_keyword.loc[len(df_keyword)] = df

            #review keyword db insert
            engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                            .format(user="root",
                                    pw="1234",
                                    db="copang_analysis"))

            df_keyword.to_sql(con=engine, name='keyword_table',if_exists='append', index=False)
            print("분석 및 키워드 저장 완료")
            break


        else:
            print("이미 분석 완료된 상품입니다.")
            break



    # def sentiment_predict(new_sentence):
    #     #불용어 리스트 가져오기
    #     f = open("stopword.txt","r")
    #     stopwords = []
    #     while True:
    #         line = f.readline().strip()
    #         if not line: 
    #             break
    #         stopwords.append(line)

