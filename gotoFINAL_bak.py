# coding=<utf-8>
# import os
# cwd = os.getwd()
import time

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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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

# argvList = [];	
# argvList.append(sys.argv[1])
# argvList.append(sys.argv[2])
# argvList.append(sys.argv[3])
# argvList.append("search")




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
		
def draw_wordcloud(text, year, subj, subjseq):

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
	plt.savefig(subj + "_" + year + "_" + subjseq + "_" + "wordcloud.png")
	plt.close('all');
				

				tokenizing

############################
# # 뽑을 데이터 년도 입력

yearList = ['2015']

for year in yearList:
	params = {'p_year' : year, 'p_job' : "search"}
	URL = 'http://ehrd.kbstar.com/pr/!kbm_aitxt.saSulData_subj'
	headers = {'Content-Type':'application/json ; charset=utf-8'}
	res = requests.get(URL, params=params, headers=headers)

	subjList = res.text
	subjList = subjList[:-3]
	subjList = subjList.replace('\n','')
	subjList = subjList.replace('\t','')
	subjList = subjList.split(', ')
	print(subjList)
	print(type(subjList))

	# subjList = ['1316242', '1316243', '1316244', '1316245', '1316368', '1316369', '1319155', '1999107', '3216345', '4216871']  

	for i in subjList:
	
		if i == '1111079' or i == '1111080' or i == '1111381' or i == '1111404' or i == '1112023' or i ==  '1112430' or i == '1113406' or i == '1113407' or i == '1115429' or i ==  '1119134' or i == '1119428' or i == '1141375' or i == '1211059' or i == '1211368' or i == '1211507' or i == '1211509' or i == '1211510' or i == '1211511' or i == '1211512' :		
			print(" 이미 처리한 과목 : " + i )
		else:
			params = {'p_year' : year, 'p_subj' : i, 'p_job' : "search"}
			URL = 'http://ehrd.kbstar.com/pr/!kbm_aitxt.saSulData_subjseq'
			headers = {'Content-Type':'application/json ; charset=utf-8'}
			res = requests.get(URL, params=params, headers=headers)
			
			subjseqList = res.text
			subjseqList = subjseqList[:-3]
			subjseqList = subjseqList.replace('\n','')
			subjseqList = subjseqList.replace('\t','')
			subjseqList = subjseqList.split(', ')
			print(subjseqList)
			print(type(subjseqList))
			
			# subjseqList = ['0003']
			
			## 최종 3중루프
			for j in subjseqList:
				params = {'p_subj' : i, 'p_year' : year, 'p_subjseq' : j, 'p_job' : "search"}
				URL = 'http://ehrd.kbstar.com/pr/!kbm_aitxt.saSulData'
				headers = {'Content-Type':'application/json ; charset=utf-8'}
				res = requests.get(URL, params=params, headers=headers)
				
				lastResult = res.text
				lastResult = lastResult[:-6]
				lastResult = lastResult+']}'
				
				## 최종 데이터셋을 제이슨의 리스트로 던져줌... 
				# print(lastResult)
				
				print(type(lastResult))
					
				# "제이슨 형식의 문자열"을 LOAD하여 "제이슨"으로 만든다.
					
				# 오류나는 건의 과목 코드, 차수를 알아야함
				print(i+"_"+year+"_"+j+"json.loads(제이슨화)시작")
			
				try:
					jsonString = json.loads(lastResult, strict=False)
				except:
					print("제이슨규격에 어긋납니다. 나중에 확인해서 따로 돌리세요.")
					print("제이슨규격에 어긋납니다. 나중에 확인해서 따로 돌리세요.")

				wordCloudStr = ""
				# 제이슨의 리스트에서 sultext만 뽑아서 워드클라우드 생성 후 저장
				for m in jsonString.get('users'):
					wordCloudStr = wordCloudStr + " " + m.get('seltext')

				# 워드클라우드생성 호출
				try:
					draw_wordcloud(wordCloudStr, year, i, j )
				except:
					print("단어가 없으므로 생성 하지 못했습니다.")
					continue

				print("업데이트 요청들어간다")
					
				for l in jsonString.get('users'):
					# 건건이 리스트를 초기화해서 새로 만들어서 바로바로 보내야함 
					# print(i)
					List = [];
					List.append(l.get('resno'))
					List.append(l.get('subj'))
					List.append(l.get('year'))
					List.append(l.get('subjseq'))
					List.append(l.get('sulnum'))
					List.append(l.get('selnum'))
					List.append(l.get('sulmasid'))
					List.append(l.get('suldetid'))
					List.append(l.get('seqno'))
					predict_pos_text(l.get('seltext'))
					#URL = 'http://ehrd.kbstar.com/pls/cyber/z_wootest.test_text2?p_resno='+List[0]+'&p_subj='+List[1]+'&p_year='+List[2]+'&p_subjseq='+List[3]+'&p_sulnum='+List[4]+'&p_selnum='+List[5]+'&p_sulmasid='+List[6]+'&p_suldetid='+List[7]+'&p_seqno='+List[8]+'&p_seltext='+List[9]+'&p_emotion='+List[10]+'&p_score='+List[11]
					URL = 'http://ehrd.kbstar.com/pls/cyber/kbm_aitxt.saResUpdate?p_resno='+List[0]+'&p_subj='+List[1]+'&p_year='+List[2]+'&p_subjseq='+List[3]+'&p_sulnum='+List[4]+'&p_selnum='+List[5]+'&p_sulmasid='+List[6]+'&p_suldetid='+List[7]+'&p_seqno='+List[8]+'&p_emotion='+List[10]+'&p_score='+List[11]
					time.sleep(0.05)
					#requests.get(URL, timeout=10000)
					page = ''
					while page == '':
						try:
							page = requests.get(URL)
							break
						except:
							print("Connection refused by the server..")
							print("Let me sleep for 5 seconds")
							print("ZZzzzz...")
							time.sleep(5)
							print("Was a nice sleep, now let me continue...")
							continue
				print( i + "_" + year + "_" + j)
				print("업데이트 요청 완료")
		
		
		
		
# ## DATA가져오기 

# list1 = ['2020']
# # list2 = ['1211517','9991012','1221012','1219535','1212540','1119441']
# list2 = ['1221012']
# list3 = ['0002']

# for i in list1:
	# # year list에서 각 year에 맞는 subj을 가져오자
	# for j in list2:
		# # subj list에서 각 subj에 맞는 subjseq를 가져오자
		# for k in list3:
			# params = {'p_subj' : j, 'p_year' : i, 'p_subjseq' : k, 'p_job' : "search"}
			# URL = 'http://ehrd.kbstar.com/pr/!kbm_aitxt.saSulData'
			# headers = {'Content-Type':'application/json ; charset=utf-8'}
			# res = requests.get(URL, params=params, headers=headers)


			# #### 파이썬 로그 찍기 잘 수행했는지... ####
			 
			# # 받은 데이터를 JSON화 하는 작업.
			# # result = ""
			# result = res.text
			# result = result[:-6]
			# result = result+']}'
	
			
			# print("타입체크")
			# print(type(result))
			
			# # "제이슨 형식의 문자열"을 LOAD하여 "제이슨"으로 만든다.
			
			# # 오류나는 건의 과목 코드, 차수를 알아야함
			# print(j+"_"+i+"_"+k+"json.loads(제이슨화)시작")
			
			# jsonString = json.loads(result, strict=False)

			# wordCloudStr = ""
			# # 제이슨의 리스트에서 sultext만 뽑아서 워드클라우드 생성 후 저장
			# for m in jsonString.get('users'):
				# wordCloudStr = wordCloudStr + " " + m.get('seltext')

			# # 워드클라우드생성 호출
			# draw_wordcloud(wordCloudStr, i, j, k)
			

			# print("업데이트 요청들어간다")
			# for l in jsonString.get('users'):
				# # 건건이 리스트를 초기화해서 새로 만들어서 바로바로 보내야함 
				# # print(i)
				# List = [];
				# List.append(l.get('resno'))
				# List.append(l.get('subj'))
				# List.append(l.get('year'))
				# List.append(l.get('subjseq'))
				# List.append(l.get('sulnum'))
				# List.append(l.get('selnum'))
				# List.append(l.get('sulmasid'))
				# List.append(l.get('suldetid'))
				# List.append(l.get('seqno'))
				# predict_pos_text(l.get('seltext'))
				# #URL = 'http://ehrd.kbstar.com/pls/cyber/z_wootest.test_text2?p_resno='+List[0]+'&p_subj='+List[1]+'&p_year='+List[2]+'&p_subjseq='+List[3]+'&p_sulnum='+List[4]+'&p_selnum='+List[5]+'&p_sulmasid='+List[6]+'&p_suldetid='+List[7]+'&p_seqno='+List[8]+'&p_seltext='+List[9]+'&p_emotion='+List[10]+'&p_score='+List[11]
				# URL = 'http://ehrd.kbstar.com/pls/cyber/kbm_aitxt.saResUpdate?p_resno='+List[0]+'&p_subj='+List[1]+'&p_year='+List[2]+'&p_subjseq='+List[3]+'&p_sulnum='+List[4]+'&p_selnum='+List[5]+'&p_sulmasid='+List[6]+'&p_suldetid='+List[7]+'&p_seqno='+List[8]+'&p_emotion='+List[10]+'&p_score='+List[11]
				# requests.get(URL, timeout=1000)
			# print( j + "_" + i + "_" + k)
			# print("업데이트 요청 완료")
			
			# ## 건건이 로그 실패한것만 키값들로어떤게 실패했는지 


	












