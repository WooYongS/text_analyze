# coding=<utf-8>
# import os
# cwd = os.getwd()

from konlpy.tag import Okt
from datetime import datetime
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from pprint import pprint
import numpy as np
import urllib.parse
import xml.sax.saxutils as saxutils

from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics

import sys

## model save 
from keras.models import load_model

## wordcloud 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from eunjeon import Mecab
from collections import Counter



okt = Okt()


import requests


# # # 하나의 문장을 토큰화 한 후 텍스트와 품사태깅을 / 구분자로 묶어준다.
def tokenizing(docs):
    return ['/'.join(t) for t in okt.pos(docs,norm=True, stem=True)]

import nltk

f = open("C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\nsmc-master\\text_final.txt", 'r', encoding='UTF8')
stringdata = f.read()
stringdata = stringdata[2:-2]
selected_words = stringdata.split('\', \'\', \'')
selected_words = stringdata.split('\', \'')


# node로부터 받은 인자값(subj, year, subjseq)을 배열에 담고 
# 해당하는 DATA http.get 으로 가져오기 ! 

argvList = [];	
argvList.append(sys.argv[1])
argvList.append(sys.argv[2])
argvList.append(sys.argv[3])
argvList.append("search")




# term_frequency()함수는 위에서 만든 selected_words의 갯수에 따라서 각 리뷰와 매칭하여 상위 텍스트가 
# 각 리뷰에 얼만큼 표현되는지 빈도를 만들기 위한 함수
def term_frequency(doc):
    return [doc.count(word) for word in selected_words]


# 모델 가져오기 
model = load_model('C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\nsmc-master\\my_model_final.h5')

def predict_pos_text(text):
	token = tokenizing(text)
	tf = term_frequency(token)
	data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
	score = float(model.predict(data))
	List.append(text)
	if(score > 0.5):
		List.append("GOOD")
		byul = str(round(score,2))
		List.append(byul)
	else:
		List.append("BAD")
		byul = str(round(score,2))
		List.append(byul)
		
def draw_wordcloud(text):

	text = text.replace('\n','')
	text = text.replace('\t','')
	
	#konlpy, Mecab : 형태소 분석을 통해 본문에서 명사추출, 1글자 단어는 삭제?
	engine = Mecab()
	nouns = engine.nouns(text)
	nouns = [n for n in nouns if len(n) > 1]
	
	# Coynter : 단어수 세기, 가장 많이 등장한 단어(명사) 30개
	count = Counter(nouns)
	tags = count.most_common(10000)
	# print(tags)
	
	#WordCloud, matplotlib: 단어 구름 그리기
	font_path = 'NanumBarunGothic.ttf'
	wc = WordCloud(font_path=font_path,background_color='white',width=800, height=600)
	# 빈도수로 워드클라우드 생성
	cloud = wc.generate_from_frequencies(dict(tags))
	
	# cloud = wc.generate(text)
	plt.figure(figsize=(10,8))
	plt.axis('off')
	plt.imshow(cloud)
	#plt.savefig('wordcloud.png')
	# 대량의 이미지를 생산할 때는..바로바로 subj,year,subjseq를 받아와야겠다.
	plt.savefig(argvList[0] + '_' + argvList[1] + '_' + argvList[2] + '_' + 'wordcloud.png')
				

				
		
## DATA가져오기 


params = {'p_subj' : argvList[0], 'p_year' : argvList[1], 'p_subjseq' : argvList[2], 'p_job' : argvList[3]}
URL = 'http://ehrd.kbstar.com/pr/!kbm_aitxt.saSulData'
headers = {'Content-Type':'application/json ; charset=utf-8'}
res = requests.get(URL, params=params, headers=headers)
#### 파이썬 로그 찍기 잘 수행했는지... ####
 
# 받은 데이터를 JSON화 하는 작업.
result = res.text
result = result[:-6]
result = result+']}'

# "제이슨 형식의 문자열"을 LOAD하여 "제이슨"으로 만든다.
jsonString = json.loads(result, strict=False)

wordCloudStr = ""
# 제이슨의 리스트에서 sultext만 뽑아서 워드클라우드 생성 후 저장
for k in jsonString.get('users'):
	wordCloudStr = wordCloudStr + " " + k.get('seltext')

# 워드클라우드생성 호출

# draw_wordcloud(wordCloudStr)



for i in jsonString.get('users'):
	# 건건이 리스트를 초기화해서 새로 만들어서 바로바로 보내야함 
	# print(i)
	List = [];
	List.append(i.get('resno'))
	List.append(i.get('subj'))
	List.append(i.get('year'))
	List.append(i.get('subjseq'))
	List.append(i.get('sulnum'))
	List.append(i.get('selnum'))
	List.append(i.get('sulmasid'))
	List.append(i.get('suldetid'))
	List.append(i.get('seqno'))
	predict_pos_text(i.get('seltext'))
	#URL = 'http://ehrd.kbstar.com/pls/cyber/z_wootest.test_text2?p_resno='+List[0]+'&p_subj='+List[1]+'&p_year='+List[2]+'&p_subjseq='+List[3]+'&p_sulnum='+List[4]+'&p_selnum='+List[5]+'&p_sulmasid='+List[6]+'&p_suldetid='+List[7]+'&p_seqno='+List[8]+'&p_seltext='+List[9]+'&p_emotion='+List[10]+'&p_score='+List[11]
	URL = 'http://ehrd.kbstar.com/pls/cyber/kbm_aitxt.saResUpdate?p_resno='+List[0]+'&p_subj='+List[1]+'&p_year='+List[2]+'&p_subjseq='+List[3]+'&p_sulnum='+List[4]+'&p_selnum='+List[5]+'&p_sulmasid='+List[6]+'&p_suldetid='+List[7]+'&p_seqno='+List[8]+'&p_emotion='+List[10]+'&p_score='+List[11]
	requests.get(URL)
## 건건이 로그 실패한것만 키값들로어떤게 실패했는지 


print("success")

	












