# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 14:11:48 2017

@author: laman
"""


import requests
import re
from bs4 import BeautifulSoup


def urlparser(keyword):
    headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate',
    'Accept-Language':'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'174',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'bbs_read_18_77097=Y; JSESSIONID=RfsRnRG8E4IbDCe8nLrSKg+7.node10',
    'Host':'www.motie.go.kr',
    'Origin':'http://www.motie.go.kr',
    'Referer':'http://www.motie.go.kr/motie/ne/presse/press2/bbs/bbsList.do',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.59 Safari/537.36'}
    payload={'bbs_cd_n':'81',
    #str(10*page+1),
    'start_dt_d':'2014-01-01',
    'end_dt_d':'2017-01-01',
    'search_key_n':'content_l',
    'search_val_v':keyword}
    url='http://www.motie.go.kr/motie/ne/presse/press2/bbs/bbsList.do'    
    plinkheader='http://www.motie.go.kr/motie/ne/presse/press2/bbs/'
    soup=BeautifulSoup(requests.post(url, headers=headers,data=payload).text,'lxml')
    pagenum=int(int(soup.find('div',class_='brdTop').find('span').text)/10)    
    pageurl=[plinkheader+i.find('a')['href'] for i in soup.find_all('td',class_='al')]
    for i in range(1, pagenum+1):
        payload['currentPage']=str(10*i+1)
        soup=BeautifulSoup(requests.post(url, headers=headers,data=payload).text,'lxml')
        pageurl+=[plinkheader+i.find('a')['href'] for i in soup.find_all('td',class_='al')]
    
    return pageurl

keyword=['원자력','원전']
url_list=[]
for i in keyword:
    url_list+=urlparser(i)
    
def unique_list(l):
    x = []
    for a in l:
        if a not in x:
            x.append(a)
    return x   

url_list=unique_list(url_list)
    
def extractarticle(url):
    print(url)
    soup=BeautifulSoup(requests.get(url).text, 'lxml')
    article=re.sub("[^가-힣]"," ",soup.find('div',class_='contTx').text)
    press='산자부'
    pubtime=[i.text for i in soup.find_all('td') if bool(re.search('\d{4}-\d{2}-\d{2}',i.text))==True][0]
    
    return pubtime, press, article
    
with open('NuclearEnergy/Data/motie.csv','w', encoding='UTF8') as f:  
    for i in url_list:
        f.write('"{0}","{1}","{2}"\n'.format(extractarticle(i)[0],extractarticle(i)[1],extractarticle(i)[2]))
    
    