# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 17:34:25 2017

@author: laman
"""

from konlpy.tag import Twitter 
import re
pos_tagger = Twitter()
def pos(doc): 
    return [t[0] for t in pos_tagger.pos(doc, norm=True, stem=True) if 'Noun' in t[1] and len(t[0])>1 ]


import pandas as pd

namelist=['chosun','chungang','khnp']
namelist=['knea','motie','nssc','navernews','navernewsadd']

total=pd.DataFrame({'pubtime':[],'press':[],'article':[]})

for i in namelist:
    #total=pd.concat([total, pd.read_csv('NuclearEnergy/Data/'+i+'.csv',index_col=0, header=0)], ignore_index=True)
    total=pd.concat([total, pd.read_csv('NuclearEnergy/Data/'+i+'.csv',names=['pubtime','press','article'])], ignore_index=True)

total=total[total['pubtime'].str.contains('2013|2017')!=True]
total=total[total['press'].str.contains('레이디경향|무비위크|씨네21|월간 산|ZDNet Korea')!=True]
total['press']=total['press'].str.replace('SBS 뉴스','SBS').str.replace('연합뉴스TV','연합뉴스').str.replace('한국경제TV','한국경제')
total['pubtime'] = total['pubtime'].str.rsplit('-', expand=True, n=1)
total = total[total['pubtime'] != '﻿"2014-01']
l = []
for i in total['article']:
    n = 0
    if '국장' in i:
        n += 1
        if '승진' in i:
            n += 1
            if '본부' in i:
                n += 1
                if '전보' in i:
                    n += 1
                    if '지사' in i:
                        n += 1
    if n > 2:
        l += [i]

for i in l:
    total = total[total['article'].str.contains(i) != True]

total=total[total['article'].str.contains('포켓몬')!=True]

total = total.drop_duplicates()
total = total.reset_index(drop=True)

total.to_csv('NuclearEnergy/Data/raw.csv', header=['article','press','pubtime'], 
             index = False, encoding='utf-8')
total = pd.read_csv('NuclearEnergy/Data/raw.csv', header=0)

total['article']=total['article'].str.replace('한국수력원자력', '한수원').str.replace('[^가-힣]|실장|본부|' \
        '소장|지사|과장|부장|본부장|본부|사장|센터|연합뉴스|사진|뉴시스|뉴스|기자|' \
        '무단|금지|배포|저작권|전재|앵커|보도|콘텐츠|국장|단장|승진|상무|전보|' \
        '지난|가지|오늘|이번|얘기|부분|위해|관련|대한|때문|' \
        '원자력|지난|가지|오늘|이번|얘기|부분|위해|관련|대한|때문|원전|\s\s', ' ')

#데이터 타입 정리
total['pubtime']=total['pubtime'].astype('category')
total['press']=total['press'].astype('category')

total['article']=pd.Series([pos(i) for i in total['article']])
#total=total[total['press'].str.contains('한수원|원자력문화재단|원자력안전위원회|산자부')==True]

time_slice=list(total.groupby('pubtime')['pubtime'].count())
press_num=total.groupby('pubtime')['pubtime'].count()

import pickle
with open('NuclearEnergy/Data/total.txt','wb') as p:
    pickle.dump(total, p)
    
with open('NuclearEnergy/Data/total.txt','rb') as p:
    total=pickle.load(p)


tokens = [j for i in total['article'] for j in i]
import nltk

text = nltk.Text(tokens) 

from matplotlib import font_manager, rc 
font_fname = 'c:/windows/fonts/malgun.ttf' # A font of your choice 
font_name = font_manager.FontProperties(fname=font_fname).get_name() 
rc('font', family=font_name)

import matplotlib.pyplot as plt

fig = plt.figure()
fig.set_label('test')
plt.figure(figsize=(20, 10)) 
text.plot(50)


from nltk.probability import FreqDist
freq = FreqDist(text)
fdic = {i[0]:i[1] for i in freq.most_common(50)}

pd.DataFrame.from_dict(fdic, orient='index').to_csv('nuclearenergy/result/freq.csv', encoding='utf-8')
