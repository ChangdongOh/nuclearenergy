# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 19:00:24 2017

@author: laman
"""

from bs4 import BeautifulSoup
import requests
import re
import time
import urllib.parse

#키워드, 시작 날짜, 끝 날짜 지정해서 120개 이상 댓글 달린 url 가져오기
def get_newsurl(keyword, date1, date2):
    first=("http://search.daum.net/search?w=news&req=tab&q={0}&cp=16nfco03BTHhdjCcTS&viewio=i&sd=" \
           "{1}&ed={2}&repno=0&period=u&n=10&p=1&cluster=n&DA=NNS" \
    .format(urllib.parse.quote_plus(keyword.encode('cp949')),date1,date2))

    soup=BeautifulSoup(requests.get(first).text, 'lxml')
    
        #첫 번째 페이지를 긁어온 다음
    if soup.find('span', class_='f_nb f_l')==None:
        return []
        
    else:
        pagenum=int(re.sub("건","",re.findall('[0-9]{1,3}건',soup.find('span', class_='f_nb f_l').text)[0]))
        totalpage=int(int(pagenum)/10 +1)
    #html태그 구조상 전체 건수 스트링에서 '건수'에 해당하는 부분만 긁어오기 위해 정규식 사용.
    #이를 int형태로 변환한 후 나눠준 다음에 다시 소수를 정수 형태로 변환.


        i=1
        url_list=[]
        #전체 url 리스트가 담길 리스트를 만들고
        while i<=totalpage:
            pageurl=re.sub('&p=[0-9]','&p='+str(i),first)
            soup=BeautifulSoup(requests.get(pageurl).text, 'lxml')
            #검색 결과가 나열된 문서를 긁은 다음
            url=[j.get('href') for j in soup.find_all('a',attrs={'class':'f_nb'})]
            url_list+=url
            i+=1
        
        return url_list
                
from datetime import timedelta
import datetime

date1=datetime.date(2008, 1, 1)
date2=datetime.date(2016, 12, 31)
keyword='원자력 & 원전'

url_list=[]
while date1 < date2:
    print(date1)
    iso=re.sub("-","",date1.isoformat())
    url_list+=get_newsurl(keyword, iso+'000000', iso+'235959')
    date1+=timedelta(days=+1)

def extractarticle(url):
    print(url)
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    if soup.find('span',class_='txt_info')==None and soup.find('span',class_='num ff_tahoma')==None:
        pubtime=re.sub("\.","-",re.findall("[0-9]{4}.[0-9]{2}.[0-9]{2}",soup.find('span',class_='txt_time').text)[0])
        press='중앙일보'
        article=soup.find('section').text
    elif soup.find('span',class_='num ff_tahoma')!=None:
        pubtime=re.sub("\.","-",re.findall("[0-9]{4}.[0-9]{2}.[0-9]{2}",soup.find('span',class_='num ff_tahoma').text)[0])
        press='중앙일보'
        article=soup.find('section').text        
    else:
        pubtime=re.sub("\.","-",re.findall("[0-9]{4}.[0-9]{2}.[0-9]{2}",soup.find_all('span',class_='txt_info')[-1].text)[0])
        press="중앙일보"
        article=soup.find('div',class_='news_view').text
    
    return pubtime, press, article
    
    
result={}
i=0
for j in url_list:
    result[i]=list(extractarticle(j))
    i+=1
    
from pandas import DataFrame

df=DataFrame(result).transpose()
df.to_csv('NuclearEnergy/Data/chungang.csv', header=['pubtime','press','article'])









