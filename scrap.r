## for extracting Global Economic section headlines in Yeonhap news
## 연합뉴스 내 국제경제 부분 헤드라인만 모아서 확인할 수 있게 하는 code
## R code

library(rvest)
library(stringr)


t <- 1
headlines <- NULL  ## claim headline variables
links <- NULL     ## claim links variables
dates <- NULL	## claim date variables

pageNum_max <- 2      ## number of pages intending to extract

for (i in 1:pageNum_max) {
  pagenum <- i
  
  ## setting url : in this case, yeonhap news
  url <- paste0("http://news.einfomax.co.kr/news/articleList.html?page=",pagenum,"&sc_section_code=S1N4")
  data <- read_html(url)
  
  dataExtracted <- html_nodes(data, ".table-row")
  headlinesRaw <- gsub("\t","",dataExtracted %>% html_text()) %>% strsplit("\n")
  
  linksRaw <- dataExtracted %>% html_nodes("a") %>% html_attr("href")
  
  for (k in 1:length(headlinesRaw)){
    headlines[t] <- headlinesRaw[[k]][3]
    
    dates[t] <- str_extract(headlinesRaw[[k]][6],"[0-9]+-[0-9]+-[0-9]+")    ## extract dates
    links[t] <- linksRaw[k]      ## extract links
    
    t <- t+1
   }
}

ni <- function (num, link=links){
  ## ni function is to shows its content of selected headlines
  
  url_for_content <- paste0("http://news.einfomax.co.kr",link[num])
  
  newsContent_raw <- read_html(url_for_content)
  newsContent <- html_nodes(newsContent_raw,"#article-view-content-div")
  
  newsContent <- gsub("\r","",gsub("\t","",newsContent %>% html_text())) %>% strsplit("\n")
  print(newsContent)
}


## make csv files

write.csv(headlines,"headlines.csv")  
write.csv(links,"links.csv")
write.csv(dates,"dates.csv")



