library(ggplot2)
library(dplyr)
library(stringr)
library(readr)

freq <- read_csv("result/freq.csv")
freq = cbind(as.data.frame(seq(1, 50)), freq)
names(freq) = c('seq', 'word', 'num')

ggplot(data = freq, aes(x=word, y=num)) +
  geom_bar(stat='identity', colour = '#0066CC', fill = '#0066CC',
           width = 0.5) +
  theme(panel.grid.minor = element_blank(), 
        panel.grid.major = element_line(color = "gray50", size = 0.5),
        panel.grid.major.x = element_blank(),
        panel.background = element_blank(),
        plot.title = element_text(hjust = 0.5),
        axis.ticks.length = unit(.25, "cm"),
        axis.text.x = element_text(angle = 90, vjust = 0, hjust = 2, size = 14, face = 'bold'),
        axis.ticks.y = element_blank(),
        axis.ticks.x = element_blank()) +
  scale_x_discrete(limits=freq$word) +
  labs(list(title = 'Most Frequent Words 50',
            x = 'Word', 
            y = 'Number of Use'))

ggsave('result/freq.jpg', width = 30, height=24, units="cm")

data <-read.csv('Result/result15.csv',row.names=1, stringsAsFactors = F)
names(data) = c(paste0('t', 1:15), 'words', 'num', 'press', 'time')


econtech = data$t2 + data$t5 + data$t15
envisafe = data$t7 + data$t13 + data$t10 + data$t8 + data$t12
conflict = data$t1 + data$t3 + data$t4 + data$t9 
foreign = data$t14 + data$t11 + data$t6 
data = cbind(econtech, envisafe, conflict, foreign, data[16:19])

#fix the year-month to ordinal number
data$time = data$time %>%
  str_replace('201','')
k = as.integer()
for(i in data$time){
  l = str_split(i, '-')[[1]] %>%
    as.integer()
  k = c(k, (l[1]-4)*12 + l[2])
}
data$time = k

graph = function(data, string, filename){
  
  cond = filter(data, grepl(string, press))
  cond[1:(length(cond)-4)] = cond[1:(length(cond)-4)] * cond$words * 626.2975
  result = as.data.frame(matrix(ncol = (length(cond)-1)), stringsAsFactors = F)[-1,]
  for(i in unique(cond$time)){
    leveldata = filter(cond, time == i)
    result = rbind(result, c(colSums(leveldata[1:(length(cond)-2)]), i), 
                   stringsAsFactors = F)
  }
  names(result) = c('Industry & Economy', 'Environmnet & Safety', 'Policy & Governance', 'Diplomacy & National Security', '단어 비율', '기사 숫자', 'time')
  #sort a dataframe by value of column 'time'
  result = result[with(result, order(result$time)),]
  library(reshape2)
  
  #split the dataset into two part(data & number of articles)
  d = result[-(length(cond)-3):-(length(cond)-2)]
  d = melt(d, id.vars = 'time')
  
  
  ggplot(data = d, 
         mapping = aes(x = time, y = value, fill = variable, color = variable)) + 
    geom_line(lwd = 1) +
    scale_colour_discrete(name = 'Frame') +
    theme(panel.grid.minor = element_blank(), 
          panel.grid.major = element_line(color = "gray50", size = 0.5),
          panel.grid.major.x = element_blank(),
          panel.background = element_blank(),
          plot.title = element_text(hjust = 0.5),
          axis.ticks.length = unit(.25, "cm"),
          axis.text.x = element_text(angle = 90, hjust = 1, size = 11, face='bold'),
          axis.ticks.y = element_blank(),
          axis.ticks.x = element_blank()) +
    scale_x_continuous(breaks = (c(0, 106, 275, 351,
                                   423, 477, 665, 795, 826, 876, 986, 1060)*36/1096 + 0.5),
                       labels = c('제2차 에기본', '세월호 관련 원전 안전문제',
                                  '삼척 주민투표\n고리원전 인근 주민 암 발병 원인 인정',
                                  '한수원 사이버 해킹', '월성 1호기 계속운전 결정',
                                  '한미원자력협정\n기후변화감축목표 제출\n고리 1호기 영구정지 결정\n사용후핵연료공론화위 권고안\n7차 전력수급계획\n한빛원전 검사 오류\n중저준위 방폐장 준공',
                                  '신고리 3호기 운영허가\n신월성 1/2호기 준공\n영덕원전 찬반투표',
                                  '후쿠시마 사고 5주기', '체르노빌 사고 30주기',
                                  '고준위관리기본계획 발표\n고준위관리기본계획 공청회\n신고리 5/6호기 건설승인', 
                                  '경주 지진\n지진방재 종합대책', 
                                  '월성 1~4호기 가동재개\n영화 판도라\n요르단 원자로 준공')) +
    coord_cartesian(xlim = c(-0.0001, 36), ylim = c(-max(d$value)*0.08, max(d$value)*1.11), expand = FALSE) +
    labs(list(title = paste0('Topic Size Change over Time(', filename, ')'),
              x = 'Period(Year and Month)', 
              y = 'Size of a Topic(10,000 Words)')) +
    annotate(geom = 'text', 
             x = seq(1, 36, 3),
             y = -max(d$value)*0.03, size = 2,
             label = c('1', '4', '7', '10',                          
                       '1', '4', '7', '10',
                       '1', '4', '7', '10')) +
    annotate(geom = 'text', 
             x = seq(6, 36, 12),
             y = -max(d$value)*0.06, size = 3,
             label = c('2014', '2015', '2016'))

  ggsave(paste0('result/numberofwords/', filename, '.jpg'), width = 30, height=18, units="cm")
  
  #proportion
  
  result = result[with(result, order(result$time)),]
  #recalculate the proportional rate of the each topic
  result[1:4] = result[1:4]/rowSums(result[1:4])
  
  #split the dataset into two part(data & number of articles)
  d = result[-(length(cond)-3):-(length(cond)-2)]
  d = melt(d, id.vars = 'time')
  
  
  ggplot(data = d, 
         mapping = aes(x = time, y = value, fill = variable, color = variable)) + 
    geom_line(lwd = 1) +
    scale_colour_discrete(name = 'Frame') +
    theme(panel.grid.minor = element_blank(), 
          panel.grid.major = element_line(color = "gray50", size = 0.5),
          panel.grid.major.x = element_blank(),
          panel.background = element_blank(),
          plot.title = element_text(hjust = 0.5),
          axis.ticks.length = unit(.25, "cm"),
          axis.text.x = element_text(angle = 90, hjust = 1, size = 11, face='bold'),
          axis.ticks.y = element_blank(),
          axis.ticks.x = element_blank()) +
    scale_x_continuous(breaks = (c(0, 106, 275, 351,
                                   423, 477, 665, 795, 826, 876, 986, 1060)*36/1096 + 0.5),
                       labels = c('제2차 에기본', '세월호 관련 원전 안전문제',
                                  '삼척 주민투표\n고리원전 인근 주민 암 발병 원인 인정',
                                  '한수원 사이버 해킹', '월성 1호기 계속운전 결정',
                                  '한미원자력협정\n기후변화감축목표 제출\n고리 1호기 영구정지 결정\n사용후핵연료공론화위 권고안\n7차 전력수급계획\n한빛원전 검사 오류\n중저준위 방폐장 준공',
                                  '신고리 3호기 운영허가\n신월성 1/2호기 준공\n영덕원전 찬반투표',
                                  '후쿠시마 사고 5주기', '체르노빌 사고 30주기',
                                  '고준위관리기본계획 발표\n고준위관리기본계획 공청회\n신고리 5/6호기 건설승인', 
                                  '경주 지진\n지진방재 종합대책', 
                                  '월성 1~4호기 가동재개\n영화 판도라\n요르단 원자로 준공')) +
    coord_cartesian(xlim = c(-0.0001, 36), ylim = c(-max(d$value)*0.08, 1.11), expand = FALSE) +
    labs(list(title = paste0('Topic Proportion Change over Time(', filename, ')'),
              x = 'Period(Year and Month)', 
              y = 'Proportion of a Topic')) +
    annotate(geom = 'text', 
             x = seq(1, 36, 3),
             y = -max(d$value)*0.03, size = 2,
             label = c('1', '4', '7', '10',                          
                       '1', '4', '7', '10',
                       '1', '4', '7', '10')) +
    annotate(geom = 'text', 
             x = seq(6, 36, 12),
             y = -max(d$value)*0.06, size = 3,
             label = c('2014', '2015', '2016'))
  
  ggsave(paste0('result/proportion/', filename, '.jpg'), width = 30, height=18, units="cm")
}

graph(data,"한수원|산자부|원자력문화재단|원자력안전위원회", 'Governmental Organizations')
graph(data,"한수원", 'Korea Hydro & Nuclear Power Co.,Ltd.')
graph(data,"산자부", 'Ministry of Trade, Industry and Energy')
graph(data,"원자력문화재단", 'Korea Nuclear Energy Agency')
graph(data,"원자력안전위원회", 'Nuclear Security and Security Commission')
graph(data,"", 'Total Data')
graph(data, "경향신문|국민일보|내일신문|동아일보|문화일보|서울신문|세계일보|조선일보|중앙일보|한겨레|한국일보|
뉴스1|뉴시스|연합뉴스|연합뉴스TV|채널A|한국경제TV|JTBC|KBS|MBC|MBN|SBS|TV조선|YTN|
매일경제|머니투데이|서울경제|아시아경제|이데일리|조선비즈|파이낸셜뉴스|한국경제|헤럴드경제|SBS CNBC|
노컷뉴스|데일리안|미디어오늘|오마이뉴스|쿠키뉴스|프레시안|디지털데일리|디지털타임스|블로터|아이뉴스24|전자신문|
매경이코노미|머니S|시사IN|신동아|이코노미스트|일다|주간경향|주간동아|주간조선|주간한국|중앙SUNDAY|팝뉴스|한겨레21|한경비즈니스|
강원일보|매일신문|부산일보", 'Total Media')
graph(data, "경향신문|국민일보|내일신문|동아일보|문화일보|서울신문|세계일보|조선일보|중앙일보|한겨레|한국일보", "Daily Newspaper")
graph(data, "뉴스1|뉴시스|연합뉴스|연합뉴스TV", 'News Agency')
graph(data, "채널A|한국경제TV|JTBC|KBS|MBC|MBN|SBS|TV조선|YTN", 'Broadcasting Company')
graph(data, "매일경제|머니투데이|서울경제|아시아경제|이데일리|조선비즈|파이낸셜뉴스|한국경제|헤럴드경제|SBS CNBC", "Business Newspaper")
graph(data, "노컷뉴스|데일리안|미디어오늘|오마이뉴스|쿠키뉴스|프레시안", "Internet Press")
graph(data, "디지털데일리|디지털타임스|블로터|아이뉴스24|전자신문", "IT-Digital Newspaper")
graph(data, "매경이코노미|머니S|시사IN|신동아|이코노미스트|일다|주간경향|주간동아|주간조선|주간한국|중앙SUNDAY|팝뉴스|한겨레21|한경비즈니스", "Weekly-Monthly Magazine")
graph(data, "강원일보|매일신문|부산일보", "Regional Newspaper")

graph(data, "경향신문|한겨레", "Liberal Press")
graph(data, "조선일보|동아일보", "Conservative Press")



