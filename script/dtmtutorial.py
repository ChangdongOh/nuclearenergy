# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:05:30 2017

@author: laman
"""

from gensim.models.wrappers.dtmmodel import DtmModel
import pandas as pd
import re
from gensim import models
from gensim import corpora
import pickle

with open('NuclearEnergy/Data/total.txt', 'rb') as p:
    total = pickle.load(p)

total = total[total['press'].str.contains('한수원|원자력문화재단|원자력안전위원회|산자부') == True]
time_slice = list(total.groupby('pubtime')['pubtime'].count())

dic = corpora.Dictionary(total['article'])

tf = [dic.doc2bow(i) for i in total['article']]
tfidfm = models.TfidfModel(tf)
tfidf = tfidfm[tf]

corpus = tfidf.corpus

model = DtmModel('C:/dtm-win64.exe.', corpus, time_slice,
                 num_topics=20, id2word=dic)

with open('NuclearEnergy/Result/model1.txt', 'wb') as p:
    pickle.dump(model, p)

with open('NuclearEnergy/Result/model1.txt', 'rb') as p:
    model = pickle.load(p)

for i in range(0, 36):
    doc_topic_dists = pd.DataFrame(model.dtm_vis(corpus, i)[0])
    doc_topic_dists.index.name = 'doc'
    doc_topic_dists.columns.name = 'topic'

    doc_lengths = pd.Series(model.dtm_vis(corpus, i)[2])
    doc_lengths.name = 'doc_lenghts'
    topic_freq = (doc_topic_dists.T * doc_lengths).T.sum()
    topic_freq = topic_freq/sum(topic_freq)
    print(topic_freq[3])


