import os
import sys
import urllib.request
import input_page
import analysis
import pandas as pd
import numpy as np
import pymysql
import output_analysis
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets


import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas





def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# #메인 화면 파일 연결
main_form = resource_path("./ui/main_page.ui")
main_form_class = uic.loadUiType(main_form)[0]


#화면을 띄우는데 사용되는 Class 선언
class main_class(QMainWindow,main_form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('main')



######################################################################################################
        #input _page에서 입력받은 상품 번호 가져오기
        input_prod_num=input_page.user_num
        #입력받은 상품번호로 db 연결, 데이터 가져오기
        conn = pymysql.connect(host = 'localhost',
                            port = 3306,
                            user = 'root',
                            password = '1234',
                            db = 'copang_analysis')
        sql_input = f"SELECT * FROM prod_table where prod_num = '{input_prod_num}'"
        df_this_data = pd.read_sql_query(sql_input, conn)
######################################################################################################
        #상품 이미지 데이터
        img_link=df_this_data.iloc[0]["prod_pic"]
        urlString = img_link
        imageFromWeb = urllib.request.urlopen(urlString).read()
        #urllib로 가져온 사진데이터를 이용해 qPixmap객체에 이미지를 load하는 코드
        qPixmapVar = QPixmap()
        qPixmapVar.loadFromData(imageFromWeb)
        #img_label 부분에 lode
        self.img_label.setPixmap(qPixmapVar)
######################################################################################################
        #상품 내용 데이터
        prod_name=df_this_data.iloc[0]["prod_name"]
        prod_price=df_this_data.iloc[0]["prod_price"]
        prod_type=df_this_data.iloc[0]["prod_type"]
        #데이터 입력
        self.prod__info.setText(prod_name + "\n" + prod_price + "\n" + prod_type)
######################################################################################################
        #상품 상세 데이터
        detail_info=df_this_data.iloc[0]["detail_info"]
        #상세 데이터 "/ "를 기준으로 자르기
        cut_detail_info= detail_info.split("/ ")
        #변수 선언 
        sum_cut_detail_info = ""
        #"/ "를 기준으로 자른 데이터를 줄 바꿈해서 다시 합치기 
        for i in range(len(cut_detail_info)):
            sum_cut_detail_info = sum_cut_detail_info+cut_detail_info[i] + "\n"

        #데이터 입력
        self.detail_info.setText(sum_cut_detail_info)
######################################################################################################


    #분석시작 버튼
    def analysis_btn(self):
######################################################################################################
#analysis_box1
        #분석 완료데이터 데이터베이스에 저장까지 하는 함수
        analysis.keyword__analysis()
        #데이버베이스에 저장된 데이터를 가져와 화면에 보여주는 함수
        in_analysis_box= output_analysis.top_keyword()
        
        self.prod_keyword.clear()

        self.prod_keyword.addItems(in_analysis_box)




######################################################################################################
#analysis_box2
        #wordcloud
        qPixmapVar = QPixmap()

        output_analysis.make_wordcloud()
        qPixmapVar.load("./img/wordcloud.jpg")
        #wordcloud__img
        self.wordcloud_img.setPixmap(qPixmapVar)

        output_analysis.make_bar_chart()
        qPixmapVar.load("./img/bar_chart.jpg")
        #wordcloud__img
        self.bar_chart_img.setPixmap(qPixmapVar)




        

######################################################################################################
#analysis_box3
        for num in range(1,6):
            rating_keword = output_analysis.rating_view(num)
            if num == 5:
                self.five_rating_view.clear()
                if len(rating_keword)!=0:
                    self.five_rating_view.addItems(rating_keword)
                elif len(rating_keword) ==0:
                    self.five_rating_view.addItem("데이터 부족")

            elif num == 4:
                self.four_rating_view.clear()
                if len(rating_keword)!=0:
                    self.four_rating_view.addItems(rating_keword)
                elif len(rating_keword) ==0:
                    self.four_rating_view.addItem("데이터 부족")

            elif num == 3:
                self.thr_rating_view.clear()
                if len(rating_keword)!=0:
                    self.thr_rating_view.addItems(rating_keword)
                elif len(rating_keword) ==0:
                    self.thr_rating_view.addItem("데이터 부족")

            elif num == 2:
                self.two_rating_view.clear()
                if len(rating_keword)!=0:
                    self.two_rating_view.addItems(rating_keword)
                elif len(rating_keword) ==0:
                    self.two_rating_view.addItem("데이터 부족")

            elif num == 1:
                self.one_rating_view.clear()
                if len(rating_keword)!=0:
                    self.one_rating_view.addItems(rating_keword)
                elif len(rating_keword) ==0:
                    self.one_rating_view.addItem("데이터 부족")
######################################################################################################




#상품키워드 누르면 키워드가 들어간 리뷰를 아래 박스에 보여줌
    def keywordToreview(self):
        self.keyword_in_review.clear()
        #선택된 키워드 체크
        select_keyword=self.prod_keyword.currentItem().text()
        keywordinreview = output_analysis.keywordinreview(select_keyword)

        self.keyword_in_review.addItems(keywordinreview)




######################################################################################################

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #WindowClass의 인스턴스 생성
    myWindow = input_page.input_class()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()