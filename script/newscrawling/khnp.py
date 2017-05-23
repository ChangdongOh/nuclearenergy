# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 00:24:58 2017

@author: laman
"""


from bs4 import BeautifulSoup
import requests
import re
import urllib.parse

docnums=[]
for i in range(1, 41):
    url="http://www.khnp.co.kr/board/BRD_000187/boardMain.do?pageIndex={0}&boardSeq=&mnCd=FN0702&schPageUnit=10" \
    "&searchCondition=2&searchKeyword=%EC%9B%90%EC%A0%84".format(i)

    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    docnums+=[re.sub("[^0-9]+","",i['href']) for i in soup.find_all('a') if i.find('dl',class_='img_desc col')!=None]
    
def extractarticle(docnums):    
    url="http://www.khnp.co.kr/board/BRD_000187/boardView.do?boardSeq={0}".format(docnums)
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    article=soup.find('div',class_='viewCont').text
    pubtime=re.sub("\.","-",re.findall("[0-9]{4}.[0-9]{2}.[0-9]{2}",soup.find('span',class_='colSec tit').text)[0])
    press='한수원'  
    
    return pubtime, press, article
    

   
result={}
i=0
for j in docnums:
    result[i]=list(extractarticle(j))
    i+=1
    
from pandas import DataFrame


df=DataFrame(result).transpose()
df=df[0:-5]
df.to_csv('NuclearEnergy/Data/khnp.csv', header=['pubtime','press','article'])
    




  