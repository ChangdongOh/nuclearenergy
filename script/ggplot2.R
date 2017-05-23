library(ggplot2)
library(dplyr)
library(stringr)

data <-read.csv('Result/result15.csv',row.names=1, stringsAsFactors = F)
names(data) = c(paste0('t', 1:15), 'words', 'num', 'press', 'time')
data = filter(data, press != 'ZDNet Korea')
econtech = data$t2 + data$t6 + data$t10 + data$t12 + data$t13
envisafe = data$t3 + data$t4 + data$t7 + data$t11 + data$t15
conflict = data$t1 + data$t8 + data$t14
foreign = data$t5 + data$t9

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
  cond[1:4] = cond[1:4] * cond$words
  result = as.data.frame(matrix(ncol = 7), stringsAsFactors = F)[-1,]
  for(i in unique(cond$time)){
    leveldata = filter(cond, time == i)
    result = rbind(result, c(colSums(leveldata[1:6]), i), 
                   stringsAsFactors = F)
  }
  names(result) = c('경제', '안전', '거버넌스', '외교안보', '기사 숫자', 'time')
  #sort a dataframe by value of column 'time'
  result = result[with(result, order(result$time)),]
  library(reshape2)
  
  #split the dataset into two part(data & number of articles)
  d1 = result[-5]
  d2 = result[-1:-4]
  
  d1 = melt(d1, id.vars = 'time')
  d2 = melt(d2, id.vars = 'time')
  
  names(d1)[2] = 'frame'
  names(d2)[2] = 'numbers'
  
  ggplot(data=d1, aes(x=time, y=as.numeric(value), 
                           group = frame, color = frame))+
    geom_line(stat='identity',
              lwd=2 #선의 굵기 지정
    )
  
  p1 <- ggplot(data=d1, aes(x=time, y=as.numeric(value), 
                                 group = frame, color = frame)) +
    geom_line(stat='identity', size = 1.5 ) + #선의 굵기 지정
    #theme(panel.grid.minor = element_blank(), 
     #     panel.grid.major = element_line(color = "gray50", size = 0.5),
      #    panel.grid.major.x = element_blank(),
      #    panel.background = element_blank(),
       #   axis.text.y = element_text(size = 14),
        #  axis.text.x = element_text(size = 14),
         # axis.ticks.length = unit(.25, "cm"),
          #axis.ticks.y = element_blank(),
          #plot.title = element_text(vjust=2.12, size = 14)) +
    scale_y_continuous(expand = c(0, 0), limits = c(-0.0001, 0.004)) +
    scale_x_continuous(breaks = seq(1, 36, 3), 
                       labels = c('2014', '4', '7', '10', 
                                  '2015', '4', '7', '10', 
                                  '2016', '4', '7', '10')) +
    ggtitle("Proportion of Topics") + labs(x = NULL, y = NULL)
  
  p2 <- ggplot(d2, aes(x = time, y = as.numeric(value))) +
    geom_bar(stat='identity', width = 0.5, fill = '#00A4E6') +
    theme(panel.grid.minor = element_blank(), 
          panel.grid.major = element_line(color = "gray50", size = 0.5),
          panel.grid.major.x = element_blank(),
          panel.background = element_blank(),
          axis.text.y = element_text(size = 14),
          axis.text.x = element_text(size = 14),
          axis.ticks.length = unit(.25, "cm"),
          axis.ticks.y = element_blank(),
          plot.title = element_text(hjust = 0.85, vjust=2.12, size = 14)) +
    scale_x_continuous(breaks = seq(1, 12, 4), labels = c('2014', '2015', '2016')) +
    ggtitle("Number of Articles") + labs(x = NULL, y = NULL)
  
  g1 <- ggplotGrob(p1)
  g2 <- ggplotGrob(p2)
  
  pp <- c(subset(g1$layout, name == "panel", se = t:r))
  
  g1 <- gtable_add_grob(g1, g2$grobs[[which(g2$layout$name == "panel")]], pp$t, pp$l, pp$b, pp$l)
  
  ggsave(paste0('Result/', filename, '.png'),width=30, height=12, units="cm")
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

