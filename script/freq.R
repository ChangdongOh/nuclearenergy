library(ggplot2)
library(dplyr)

data <-read.csv('Result/result15new.csv',row.names=1)
names(data) = c(paste0('t', 1:15), 'words', 'num', 'press', 'time')
data = filter(data, press != 'ZDNet Korea')
econtech = data$t3 + data$t5 + data$t8 + data$t11 + data$t13
envisafe = data$t1 + data$t14
conflict = data$t10 + data$t12 + data$t15 + data$t6 + data$t4 + data$t2
foreign = data$t9

merge = cbind(econtech, envisafe, conflict, foreign, data[16:19])

freq = function(data, string, filename){
  cond = filter(data, grepl(string, press))
  result = data.frame(matrix(ncol = 2))[-1,]
  for(i in levels(factor(cond$press))){
    leveldata = filter(cond, grepl(i, press))
    result = leveldata$num %>%
      sum() %>%
      c(i) %>%
      rbind(result, stringsAsFactors = F)
    names(result) = c("num", "press")
  }
  write.csv(result, paste0('Result/freq/', filename, '.csv'))
}

freq(merge,"한수원|산자부|원자력문화재단|원자력안전위원회", '원자력계 전반')
freq(merge, "경향신문|국민일보|내일신문|동아일보|문화일보|서울신문|세계일보|조선일보|중앙일보|한겨레|한국일보", "종합일간지")
freq(merge, "뉴스1|뉴시스|연합뉴스|연합뉴스TV", '뉴스통신사')
freq(merge, "채널A|한국경제TV|JTBC|KBS|MBC|MBN|SBS|TV조선|YTN", '방송사')
freq(merge, "매일경제|머니투데이|서울경제|아시아경제|이데일리|조선비즈|파이낸셜뉴스|한국경제|헤럴드경제|SBS CNBC", "경제지")
freq(merge, "노컷뉴스|데일리안|미디어오늘|오마이뉴스|쿠키뉴스|프레시안", "인터넷 언론")
freq(merge, "디지털데일리|디지털타임스|블로터|아이뉴스24|전자신문", "IT디지털")
freq(merge, "매경이코노미|머니S|시사IN|신동아|이코노미스트|일다|주간경향|주간동아|주간조선|주간한국|중앙SUNDAY|팝뉴스|한겨레21|한경비즈니스", "주간월간지")
freq(merge, "강원일보|매일신문|부산일보", "지역언론")

freq(merge, "경향신문|한겨레", "진보")
freq(merge, "조선일보|동아일보", "보수")
