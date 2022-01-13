import time
from PIL import Image
from konlpy.tag import Okt

from pprint import pprint
import numpy as np
import urllib.parse
import xml.sax.saxutils as saxutils

import sys

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from eunjeon import Mecab
from collections import Counter

import nltk

okt = Okt()

# # # 하나의 문장을 토큰화 한 후 텍스트와 품사태깅을 / 구분자로 묶어준다.
# def tokenizing(docs):
    # return ['/'.join(t) for t in okt.pos(docs,norm=True, stem=True)]

import nltk

# term_frequency()함수는 위에서 만든 selected_words의 갯수에 따라서 각 리뷰와 매칭하여 상위 텍스트가 
# 각 리뷰에 얼만큼 표현되는지 빈도를 만들기 위한 함수
# def term_frequency(doc):
    # return [doc.count(word) for word in selected_words]

		
# 20210310_조직문화
# 20210310_경영전략
# 20210310_성과관리
# 20210310_인사복지


## 워드클라우드 컬러 커스터마이징
# def make_colors(word,font_size,position,orientation,random_state,**kwargs):
	# color = "#d4b4f8"
	# return color

	

f = open("C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\nsmc-master\\nation.txt", 'r', encoding='euc-kr')
stringdata = f.read()

	
def draw_wordcloud(text):

	## 468개 최종
	## 특정 단어 없애기
	
	text = text.replace('직원','')
	text = text.replace('금융인','')
	text = text.replace('은행','')
	text = text.replace('KB','')
	text = text.replace('조직문화','')
	text = text.replace('기업문화','')
	text = text.replace('KB','')
	
	

	
	text = text.replace('화이팅','')
	text = text.replace('시대','')
	text = text.replace('메타','')
	text = text.replace('버스','')
	text = text.replace('메타버스','')
	text = text.replace('국민은행','')
	text = text.replace('직장','')
	text = text.replace('직장내','')
	text = text.replace('KB','')
	text = text.replace('괴롭힘','')
	text = text.replace('성희롱','')
	text = text.replace('우리','')
	text = text.replace('조직','')
	text = text.replace('만큼','')
	text = text.replace('누구','')
	text = text.replace('만큼','')
	text = text.replace('경우','')
	text = text.replace('마디','')
	text = text.replace('겁니다','')
	

	
	
	# text = text.replace('지점장','수평')
	# text = text.replace('직원','리더십')
	# text = text.replace('영업','커뮤니케이션')
	# text = text.replace('경영진','로열티')
	# text = text.replace('부여','갈등')
	# text = text.replace('바퀴','부여')
	# text = text.replace('관련','')
	# text = text.replace('추진','')
	# text = text.replace('타결','')
	# text = text.replace('경우','')
	# text = text.replace('중요','')
	# text = text.replace('말씀','')
	# text = text.replace('경영','')
	# text = text.replace('은행장','')
	# text = text.replace('체크','')
	# text = text.replace('행장','')
	# text = text.replace('중앙','')
	# text = text.replace('노동','')
	# text = text.replace('위원회','')
	# text = text.replace('조정','')
	# text = text.replace('아래','')
	# text = text.replace('로비','')
	# text = text.replace('매니저','')
	# text = text.replace('방법','')
	
	# text = text.replace('생각','')
	# text = text.replace('필요','')
	# text = text.replace('은행장','')
	# text = text.replace('행장','')
	# text = text.replace('말씀','')
	# text = text.replace('가능','')
	# text = text.replace('이야기','')
	# text = text.replace('내용','')
	# text = text.replace('무엇','')
	# text = text.replace('만약','')
	# text = text.replace('대부분','')
	# text = text.replace('지점장','')
	# text = text.replace('사례','')
	# text = text.replace('별도','')
	
	# text = text.replace('계획','코로나')
	# text = text.replace('축소','전결')
	# text = text.replace('지점','')
	# text = text.replace('점포','')
	# text = text.replace('고객','')
	# text = text.replace('관련','')
	# text = text.replace('필요','')
	# text = text.replace('단순','')
	# text = text.replace('직원','')
	# text = text.replace('경우','')
	# text = text.replace('고려','')
	# text = text.replace('수도','')
	# text = text.replace('점주','')
	# text = text.replace('발 생','')
	# text = text.replace('부족','')
	# text = text.replace('어려움','')
	# text = text.replace('별도','')
	
	## 특정 단어 없애기
	
	text = text.replace('\n','')
	text = text.replace('\t','')
	
	engine = Mecab()
	nouns = engine.nouns(text)
	nouns = [n for n in nouns if len(n) > 1]
	
	count = Counter(nouns)
		
	######## 몇개의 단어 추출할 건지 설정 ##########
	tags = count.most_common(100)
	######## 몇개의 단어 추출할 건지 설정 ##########
	
	print(tags)
	
	#WordCloud, matplotlib: 단어 구름 그리기
	font_path = 'KBFGTextM.ttf'
	# wc = WordCloud(font_path=font_path,background_color='white',mask = cloud_mask,width=800, height=600)
	
	wc = WordCloud(font_path=font_path,background_color='white',width=800, height=600)
	
	# 빈도수로 워드클라우드 생성
	cloud = wc.generate_from_frequencies(dict(tags))
	
	## color customizing
	# cloud = cloud.recolor(color_func=make_colors,random_state=True)
	
	# cloud = wc.generate(text)
	plt.figure(figsize=(10,8))
	plt.axis('off')
	plt.imshow(cloud, interpolation='lanczos')
	#plt.savefig('wordcloud.png')
	
	######### 생성될 이미지 파일명 #########
	plt.savefig("nation.png")
	######### 생성될 이미지 파일명 #########
	
	plt.close('all');
	
# cloud_mask = np.array(Image.open("cloudmask2.png"))

draw_wordcloud(stringdata)






