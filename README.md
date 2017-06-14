Nuclear Energy Discourse of South Korea: an Analysis Based on Author-Topic Models
===============
Changdong Oh(with Teajun Lee, Seungbae Lee, Huekyung Won)

Summary
-----------
I collected korean newspaper articles related to nuclear energy and analyzed the articles by Author-topic Model. By this analysis, researchers try to expore the nuclear energy discourse of south korea and critically review the existing analysis frames of earlier works. Furthermore, based on the result of my analysis, collaborators suggest an alternative analytic frame for nuclear energy and crisis management.

Data
--------
In this research, I gathered 29565 newspaper articles to analyze public opinion toward nuclear energy according to two criteria. First, it should contain words 'nuclear energy(원자력)' or 'nuclear power(원전)' to pick only relevant articles. Second, I restricted the period of article from 2014 to 2016. In the data collecting process, I used the Naver and Daum, which are the largest internews news portal sites in South Korea.

Additionally, I collected 925 official announcements of several governmental organizations related to the nuclear energy industry of south korea.

Codes used in this procedure are saved on script/newscrawling folder.

Preprocess
-------
With the [KoNLPy](http://konlpy.org/en/v0.4.4/) wrapper of [twitter korean morpheme analyzer](https://github.com/twitter/twitter-korean-text), I seperated the collected news articles into morpheme units and left only noun, and removed some meaningless stopwords. After the preprocess, I visualized the most frequently used words in my text data.

![wordfrequency](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/freq.jpg)

Analysis
--------
I adopted an Author-Topic Model[(Rosen-Zvi et al. 2004)](http://dl.acm.org/citation.cfm?id=1036902), which is well-known modified algorithm of Latent Dirichlet Allocation. Today LDA is widely used by social scientists. With this algorithm alone, however, it is hard to do more than exploratory research for large text data. To solve the problem, many algorithms such as DTM, DMR, STM are suggested and ATM is one of them. With this algorithm, we can see the propotional changes of topic by author. In this study, I regarded the publisher(or organization) of article and the time of publication as an 'author', for example, tagging articles in the form of 'Korea Joongang Daily-2016-1'. I used the [python wrapper of ATM](https://radimrehurek.com/gensim/models/atmodel.html), which was announced recently. The authornamelda.py file of script folder is my code used in the analysis process.

Result
---------
