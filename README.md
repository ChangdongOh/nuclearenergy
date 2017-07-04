Nuclear Energy Discourse of South Korea: an Analysis Based on Author-Topic Models
===============
Changdong Oh(with Teajun Lee, Seungbae Lee, Huekyung Won)

Summary
-----------
I collected Korean newspaper articles related to nuclear energy and analyzed the articles by Author-topic Model. By this analysis, researchers try to explore the nuclear energy discourse of south korea and critically review the existing analysis frames of earlier works. Furthermore, based on the result of my analysis, collaborators suggest an alternative analytic frame for nuclear energy and crisis management.

Data
--------
In this research, I gathered 29565 newspaper articles to analyze public opinion toward nuclear energy according to two criteria. First, it should contain words 'nuclear energy(원자력)' or 'nuclear power(원전)' to pick only relevant articles. Second, I restricted the period from 2014 to 2016. In the data collecting process, I used the Naver and Daum, which are the largest internet news portal sites in South Korea.

Additionally, I collected 925 official announcements of several governmental organizations related to the nuclear energy industry of south korea.

Codes used in this procedure are saved on script/newscrawling folder.

Preprocess
-------
With the [KoNLPy](http://konlpy.org/en/v0.4.4/) wrapper of [twitter korean morpheme analyzer](https://github.com/twitter/twitter-korean-text), I separated the collected news articles into morpheme units and left only noun, and removed some meaningless stopwords. After the preprocess, I visualized the most frequently used words in my text data. You could review the codes that I used in this task on the script/preporcess.py file.

![wordfrequency](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/freq.jpg)

Analysis
--------
I adopted an Author-Topic Model[(Rosen-Zvi et al. 2004)](http://dl.acm.org/citation.cfm?id=1036902), which is the well-known modified algorithm of the Latent Dirichlet Allocation. Today LDA is widely used by social scientists. With this algorithm alone, however, it is hard to do more than exploratory research for large text data. To solve the problem, many algorithms such as DTM, DMR, STM are suggested and ATM is one of them. With this algorithm, we can see the proportional changes of each topic by each author. In this study, I regarded the publisher(or organization) and the time of publication as an 'author', for example, tagging articles in the form of 'Korea Joongang Daily-2016-1'. I used the [python wrapper of ATM](https://radimrehurek.com/gensim/models/atmodel.html), which was announced recently. The authornamelda.py file of script folder is my code used in the analysis process.

Result
---------

#### Topics
After the analysis based on ATM, the algorithm suggested a composition of topics in the text data and proportion of words of each topic. You could see the well-organized table form of the topic composition in [topics15.csv](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/topics15.csv) file.

My collaborators reviewed the distribution of topics and words and suggested a new framework for combining the 15 topics because there are several overlapping and similar topics are in our analysis result. Topics can be organized by four frames, Policy & Governance, Economy & Industry, Environment & Safety, Diplomacy & Security according to the framework. I classified the topics by this framework and analyzed the difference of frames by time period and publisher. Additionally, I suggested the visualized analysis data by two part(proportional size of topics in the period, the absolute size of topics in the period) due to the fact that the number of news articles was changed significantly over time. You could see those graphs on [proportion](https://github.com/ChangdongOh/nuclearenergy/tree/master/result/proportion), [nofwords](https://github.com/ChangdongOh/nuclearenergy/tree/master/result/nofwords) folders in the result folder. 

The red line means the industry, economy related topics, and the green describes environment and safety problem. The Third turquoise line shows topics related to policy and governance, and the last means diplomacy and national security topics. 

The following plots are the results which are interesting for me.

##### Attitude Difference of Press Companies and Governmental Organizations?
![newpub](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/nofwords/%EC%96%B8%EB%A1%A0%EC%82%AC%20%EC%A0%84%EC%B2%B4.jpg)
![govorg](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/nofwords/%EC%9B%90%EC%9E%90%EB%A0%A5%EA%B3%84%20%EC%A0%84%EB%B0%98.jpg)

Two graphs reveals that the governmental organization and media were responding differently to important events and affairs. To be specific, the organizations tended to pay more attention to the economic issues.

##### Business Newspapers
![eco](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/nofwords/%EA%B2%BD%EC%A0%9C%EC%A7%80.jpg)

Understandably, business newspapers concerned the topics related to the nuclear energy industry and ecomic problems.

##### Regional Newspapers
![reg](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/nofwords/%EC%A7%80%EC%97%AD%EC%96%B8%EB%A1%A0.jpg)

Regional newspapers covered more issues related to the policy, conflict and governance. They seems to represent a local residents, who are direct stakeholders of the nuclear energy.

##### Liberals concern safety and governance, Conservatives concern economy?
![lib](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/nofwords/%EC%A7%84%EB%B3%B4.jpg)
![con](https://github.com/ChangdongOh/nuclearenergy/blob/master/result/nofwords/%EB%B3%B4%EC%88%98.jpg)


Future Research Plan
------

We are trying hard to finish a first paper based on my analysis. I found many interesting characteristics and dispositions of each newspaper company and govermental organization, so I want to try a follow-up study which can be used to elaborate my analysis. My co-authors suggested that Semantic Network Analysis(SNA) can be useful to expatiate our analysis result, but now I consider that semi-supervised sentiment analysis using topic model is better and more decisive way to amplify the meaning of our work.