# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 00:32:15 2017

@author: laman
"""

from bs4 import BeautifulSoup
import requests
import re
import urllib.parse

#키워드, 시작 날짜, 끝 날짜 지정해서 120개 이상 댓글 달린 url 가져오기
def get_newsurl(keyword, date1, date2):
    first=("http://news.naver.com/main/search/search.nhn?query={0}&st=" \
"news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=all.basic&ic=all&so=rel.dsc&" \
"rcnews=exist:032:005:086:020:021:081:022:023:025:028:038:469:421:003:001:422:449:004:215:437" \
":056:214:019:057:096:374:055:448:052:009:008:011:277:018:366:014:015:016:375:079:119:006:047:143:002:087:088:082" \
":&rcsection=exist:&stDate=range:20140101:20140101&detail=0&pd=4&r_cluster2_start=1&r_cluster2_display=10&" \
"start=1&display=10&startDate={1}&endDate={2}&page=" \
    .format(urllib.parse.quote_plus(keyword.encode('cp949')),date1,date2))

    soup=BeautifulSoup(requests.get(first).text, 'lxml')
    #첫 번째 페이지를 긁어온 다음
    if soup.find('span',class_='result_num')==None:
        return []
        
    else:
        pagenum=re.sub(',','',soup.find('span',class_='result_num').text.split('건')[0].split('/')[1][1:])
        totalpage=int(int(pagenum)/10 +1)
    #html태그 구조상 전체 건수 스트링에서 '건수'에 해당하는 부분만 긁어오기 위해 정규식 사용.
    #이를 int형태로 변환한 후 나눠준 다음에 다시 소수를 정수 형태로 변환.


        i=1
        url_list=[]
        #전체 url 리스트가 담길 리스트를 만들고
        while i<=totalpage:
            pageurl=first+str(i)
            soup=BeautifulSoup(requests.get(pageurl).text, 'lxml')
        #검색 결과가 나열된 문서를 긁은 다음
            for j in soup.find_all('a',attrs={'class':'go_naver'}):
            #네이버 자체 뉴스 페이지 링크를 긁은 다음 리스트 형태로 만들고 다시 for문에 집어넣고 나서                
                url_list.append(j.get('href'))
            i+=1 
        
        return url_list
                
from datetime import timedelta
import datetime

date1=datetime.date(2014, 1, 1)
date2=datetime.date(2016, 12, 31)
keyword='원자력 & 원전'

url_list=[]
while date1 < date2:
    print(date1)
    url_list+=get_newsurl(keyword, date1, date1)
    date1+=timedelta(days=+1)



def articlepre(article):
    split=re.split("@",article)
    if len(split)==1:
        article=split[0]
    else: article="".join(split[0:-1])    
    split=re.split("ⓒ",article)
    if len(split)==1:
        article=split[0]
    else: article="".join(split[0:-1]) 
    split=re.split("모바일 경향",article)
    if len(split)==1:
        article=split[0]
    else: article="".join(split[0:-1])     
    article=re.sub("flash 오류를 우회하기 위한 함수 추가|function _flash_removeCallback|모바일 경향|공식 SNS 계정|[^가-힣]"," ",article)
    return article


def extractarticle(url):
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    if soup.find('h4',class_='aside_tit')==None and soup.find('div',class_='aside_photo')==None:
        press=soup.find('div', class_='press_logo').find('img')['title']
        article=soup.find('div',attrs={'id':'articleBodyContents'}).text
        for i in soup.find('div',attrs={'id':'articleBodyContents'}).find_all('a'):
            article=article.replace(i.text,' ')
        article=articlepre(article)
        pubtime=re.findall('\d{4}-\d{2}-\d{2}',soup.find('span',class_='t11').text)[0]
    elif soup.find('h4',class_='aside_tit')==None:
        press=soup.find('span', class_='logo').find('img')['alt']
        article=soup.find('div',attrs={'id':'newsEndContents'}).text
        for i in soup.find('div',attrs={'id':'newsEndContents'}).find_all('a'):
            article=article.replace(i.text,' ')                         
        article=articlepre(article)                   
        pubtime=re.sub('[.]','-',re.findall('\d{4}[.]\d{2}[.]\d{2}',soup.find('div',class_='info').find_all('span')[1].text)[0])
    else:
        pubtime=re.sub("\.","-",re.findall("[0-9]{4}.[0-9]{2}.[0-9]{2}",soup.find('span',class_='author').text)[0])
        press=soup.find('a', class_='press_logo').find('img')['alt']
        article=soup.find('div',attrs={'id':'articeBody'}).text
        for i in soup.find('div',attrs={'id':'articeBody'}).find_all('a'):
            article=article.replace(i.text,' ')                         
        article=articlepre(article)
    

    return pubtime, press, article
    

with open('NuclearEnergy/Data/navernews.csv','w', encoding='UTF8') as f:  
    for i in url_list:
        f.write('"{0}","{1}","{2}"\n'.format(extractarticle(i)[0],extractarticle(i)[1],extractarticle(i)[2]))
        

