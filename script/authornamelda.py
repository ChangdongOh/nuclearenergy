# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:29:20 2017

@author: laman
"""


from gensim import corpora
from gensim import models
from gensim.models import AuthorTopicModel
from pprint import pprint
from natsort import natsorted, ns
import pandas as pd
import pickle
import re
import random

with open('nuclearenergy/data/total.txt', 'rb') as p:
    total = pickle.load(p)

dic = corpora.Dictionary(total['article'])

tf = [dic.doc2bow(i) for i in total['article']]
tfidfm = models.TfidfModel(tf)
tfidf = tfidfm[tf]

corpus = tfidf.corpus
vocnum = sum([j[1] for i in corpus for j in i])

id2doc = {total['press'][i] + ', ' + total['pubtime'][i]: [] \
          for i in range(0, len(total))}
for i in range(0, len(total)):
    pressid = total['press'][i] + ', ' + total['pubtime'][i]
    id2doc[pressid].append(i)

def topicandresult(num, corpus, id2doc, dic):

    """
    model_list = []
    for i in range(5):
        model = AuthorTopicModel(corpus = corpus, num_topics = num, id2word=dic, \
                                 author2doc = id2doc, chunksize = 2000, passes = 1, eval_every = 0, \
                                 #random_state = int(random.random()*1000),
                                 iterations=100000
                                 )
        top_topics = model.top_topics(corpus)
        tc = sum([t[1] for t in top_topics])
        model_list.append((model, tc))
    
    model, tc = max(model_list, key=lambda x: x[1])
    """
    model = AuthorTopicModel(corpus = corpus,
                             num_topics = num,
                             id2word = dic,
                             author2doc = id2doc,
                             chunksize = 2000,
                             passes = 55,
                             eval_every = 0,
                             gamma_threshold=1e-11,
                             iterations = 10000000)

    with open('NuclearEnergy/Data/' + str(num) + 'topic.model', 'wb') as p:
        pickle.dump(model, p)

    '''
    with open('NuclearEnergy/Data/' + str(num) + 'topic.model', 'rb') as p:
        model = pickle.load(p)
    '''

    pubid = pd.Series(list(set([total['press'][i] + ', ' + total['pubtime'][i]
                                for i in range(0, len(total))])), name='id', dtype='category')

    result = {'publisher': [], 'time': [], 'docnum': [], 'corpusp': []}
    for i in range(0, num):
        result[i] = []

    def proportion(pubid):
        docs = model.author2doc[pubid]
        return sum([word[1] for doc in docs for word in corpus[doc]]) / vocnum

    for i in pubid:
        result['publisher'].append(re.split(', ', i)[0])
        result['time'].append(re.split(', ', i)[1])
        cr1 = total['press'].map(lambda x: x == re.split(', ', i)[0])
        cr2 = total['pubtime'].map(lambda x: x == re.split(', ', i)[1])
        result['docnum'].append(len(total[cr1 & cr2]))
        result['corpusp'].append(proportion(i))
        topics = {j[0]: j[1] for j in model[i]}
        for j in result:
            if j in topics:
                result[j].append(topics[j])
            elif j is 'publisher' or j is 'time' or j is 'docnum' or j is 'corpusp':
                pass
            else:
                result[j].append(0)

    result = pd.DataFrame(result)
    result = result.reindex_axis(natsorted(result.columns, alg=ns.IC), axis=1)

    ratio = {}
    for i in range(0, num):
        ratio[i] = 0
    for index, row in result.iterrows():
        for i in ratio:
            ratio[i] += row[i] * row['corpusp']

    agg = sum(ratio.values())
    ratio = {i: str(ratio[i] * 100 / agg) + '%' for i in ratio}

    topics = pd.DataFrame({
                          i[0]: [re.split('\*', j)[1] + '*' + str(round(float(re.split('\*', j)[0]) * 100, 3)) + '%' for
                                 j in re.split(' \\+ ', re.sub('"', '', i[1]))] for i
                          in model.show_topics(num_topics= num, num_words=50)})
    topics.loc[30] = ratio
    topics = topics.reindex([30] + list(range(0, 30)))
    topics.index = ['토픽 비율'] + list(range(1, 31))
    '''
    topic_labels = ['1 사이버 해킹과 공격', '2 ',
                    '3 원전에 대한 비판적 담론들', '4 원전의 안전과 기술적 문제들',
                    '5 후쿠시마 원전 사고와 안전', '6 지진과 원자력 발전소 및 정치권', '7 해외 동향',
                    '8 지진과 원전 위치 지역의 불안', '9 원자력 안전과 지역사회', '10 원자력 관련 기관 인사',
                    '11 원자력을 둘러싼 정치적 갈등', '12 원전 건설 사업과 관련된 이슈', '13 고리/월성 원전',
                    '14 영화 판도라 관련', '15 원자력 산업 관리', '16 원전 관련 투자와 에너지 산업',
                    '17 사회적 이슈들과 일본 지진','18 원전 관련 기술', '19 원전에 대한 사업적 접근',
                    '20 원전과 북한, 안보']
                    '''
    topic_labels = [str(i) for i in range(1, num + 1)]
    topics.columns = topic_labels
    result.columns = topic_labels + ['형태소의 비율', '기사 숫자', '발표 기관', '발표 시기']

    return(topics, result, model)

num = 15
topics, result, model = topicandresult(num, corpus, id2doc, dic)

topics

top_topics = model.top_topics(corpus)
tc = sum([t[1] for t in top_topics])
tc

"""
topics.to_csv('NuclearEnergy/Result/topics' + str(num) + '.csv')
result.to_csv('NuclearEnergy/Result/result' + str(num) + '.csv')
"""