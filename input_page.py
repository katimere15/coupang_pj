import os
import sys
import main_page
import crawling
from PyQt5.QtWidgets import *
from PyQt5 import uic
# from sqlalchemy import create_engine


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# #메인 화면 파일 연결
input_form = resource_path("./ui/input_page.ui")
input_form_class = uic.loadUiType(input_form)[0]

#화면을 띄우는데 사용되는 Class 선언
class input_class(QDialog,QWidget,input_form_class):

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('input')


    def num_btn(self):
        global user_num
        user_num = self.num_input.text()
        self.num_input.clear()
        try:
            crawling.num_driver(user_num)
            

        except IndexError:
            QMessageBox.information(self,"다시입력","상품번호를 찾을 수 없습니다.")
        except:
            QMessageBox.information(self,"이동","이미 크롤링을 끝낸 상품입니다. 바로 분석정보 이동하실 수 있습니다.")
            self.close()
            self.main = main_page.main_class()    
            self.main.show()
        else:
            QMessageBox.information(self,"이동","크롤링 및 데이터 저장이 완료되었습니다.")
            self.close()
            self.main = main_page.main_class()    
            self.main.show()
