# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:08:59 2017

@author: laman
"""

from bs4 import BeautifulSoup
import requests
import re

first='http://www.nssc.go.kr/nssc/notice/report.jsp?mode=list&search%3Asearch_key%3Asearch=' \
'article_text&search%3Asearch_val%3Asearch=%25BF%25F8%25C0%25FC&board_no=2&pager.offset='

pagenum=11
url_list=[]
for i in range(0, pagenum):
    url=first+str(15*i)
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    plinkheader='http://www.nssc.go.kr/nssc/notice/report.jsp'
    url_list+=[plinkheader+i.find('a')['href'] for i in soup.find_all('td',class_='title')]
    
url_list=url_list[4:-5]


def extractarticle(url):
    print(url)
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    article=re.sub("[^가-힣]"," ",soup.find('div',attrs={'id':'article_text'}).text)
    press='원자력안전위원회'
    pubtime=soup.find_all('td',class_='borderB')[1].text
    
    return pubtime, press, article
        
    
    
with open('NuclearEnergy/Data/nssc.csv','w', encoding='UTF8') as f:  
    for i in url_list:
        f.write('"{0}","{1}","{2}"\n'.format(extractarticle(i)[0],extractarticle(i)[1],extractarticle(i)[2]))
           