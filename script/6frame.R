library(ggplot2)
library(dplyr)

data <-read.csv('Result/result15new.csv',row.names=1)
names(data) = c(paste0('t', 1:15), 'words', 'num', 'press', 'time')
data = filter(data, press != 'ZDNet Korea')
econ = data$t3 + data$t8 + data$t13
tech = data$t11 + data$t5
envisafe = data$t1 + data$t14
conflict = data$t10 + data$t12 + data$t15 +  data$t4
policy = data$t6 + data$t2
foreign = data$t9

merge = cbind(econ, tech, envisafe, conflict, policy, foreign, data[16:19])

graph = function(data, string, filename){
  
  cond = filter(data, grepl(string, press))
  
  result = as.data.frame(matrix(ncol = 7), stringsAsFactors = F)[-1,]
  for(i in levels(cond$time)){
    leveldata = filter(cond, grepl(i, time))
    result = rbind(result, c(colSums(leveldata[1:6]/c(leveldata$words))/sum(colSums(leveldata[1:6]/c(leveldata$words))), i), stringsAsFactors = F)
  }
  names(result) = c('경제', '기술', '안전', '거버넌스', '정책', '외교안보', 'time')
  
  library(reshape2)
  
  dataset = melt(result, id.vars='time')
  #sort a dataframe by value of column 'time'
  dataset[with(dataset, order(dataset$time)),]
  
  names(dataset)[2]='Frame'
  
  ggplot(data=dataset, aes(x=time, y=as.numeric(value), 
                           group = Frame, color = Frame))+
    geom_line(stat='identity',
              lwd=2 #선의 굵기 지정
    )+
    ggtitle(filename)+
    scale_y_continuous(name='토픽의 비율')+
    scale_x_discrete(name = '시간(분기)', labels = c('2014', '2', '3', '4', '2015', '2', '3', '4', '2016', '2', '3', '4')) 
  
  ggsave(paste0('Result/', filename, '.png'),width=20, height=12, units="cm")
}

graph(merge,"한수원|산자부|원자력문화재단|원자력안전위원회", '원자력계 전반')
graph(merge,"한수원", '한수원')
graph(merge,"산자부", '산자부')
graph(merge,"원자력문화재단", '원자력문화재단')
graph(merge,"원자력안전위원회", '원자력안전위원회')
graph(merge,"", '전체')
graph(merge, "경향신문|국민일보|내일신문|동아일보|문화일보|서울신문|세계일보|조선일보|중앙일보|한겨레|한국일보", "종합일간지")
graph(merge, "뉴스1|뉴시스|연합뉴스|연합뉴스TV", '뉴스통신사')
graph(merge, "채널A|한국경제TV|JTBC|KBS|MBC|MBN|SBS|TV조선|YTN", '방송사')
graph(merge, "매일경제|머니투데이|서울경제|아시아경제|이데일리|조선비즈|파이낸셜뉴스|한국경제|헤럴드경제|SBS CNBC", "경제지")
graph(merge, "노컷뉴스|데일리안|미디어오늘|오마이뉴스|쿠키뉴스|프레시안", "인터넷 언론")
graph(merge, "디지털데일리|디지털타임스|블로터|아이뉴스24|전자신문", "IT디지털")
graph(merge, "매경이코노미|머니S|시사IN|신동아|이코노미스트|일다|주간경향|주간동아|주간조선|주간한국|중앙SUNDAY|팝뉴스|한겨레21|한경비즈니스", "주간월간지")
graph(merge, "강원일보|매일신문|부산일보", "지역언론")

graph(merge, "경향신문|한겨레", "진보")
graph(merge, "조선일보|동아일보", "보수")

