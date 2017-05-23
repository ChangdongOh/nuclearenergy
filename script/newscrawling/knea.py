# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:54:16 2017

@author: laman
"""

import requests
import re
from bs4 import BeautifulSoup

urls=['http://knea.or.kr/bbs/board.php?bo_table=101030&page='+str(i) for i in range(1, 5)]+['http://knea.or.kr/bbs/board.php?bo_table=101010&page='+str(i) for i in range(1, 14)]+['http://knea.or.kr/bbs/board.php?bo_table=101020&page='+str(i) for i in range(1, 7)]
url_list=[]
for i in urls:
    soup=BeautifulSoup(requests.get(i).text, 'lxml')
    url_list+=[i.find('a')['href'] for i in soup.find_all('li',class_='col-sm-12 col-xs-6 ')]


def extractarticle(url):
    print(url)
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    article=re.sub("[^가-힣]"," ",soup.find('div',attrs={'id':'bo_v_con'}).text)
    press='원자력문화재단'
    pubtime='20'+re.findall('[0-9]{2}[-][0-9]{2}[-][0-9]{2}',soup.find('section',attrs={'id':'bo_v_info'}).text)[0]
    
    return pubtime, press, article


    
with open('NuclearEnergy/Data/knea.csv','w', encoding='UTF8') as f:  
    for i in url_list:
        f.write('"{0}","{1}","{2}"\n'.format(extractarticle(i)[0],extractarticle(i)[1],extractarticle(i)[2]))






