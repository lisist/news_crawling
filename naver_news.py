import pandas as pd
import bs4 as bs
import requests
import warnings
import datetime as dt

warnings.simplefilter(action='ignore', category=FutureWarning)

def naver_news():
   date = dt.datetime.now()
   to_day = date.strftime("%Y%m%d")
   page_num = 1

   url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=262&sid1=102&date='+to_day+'&page='+str(page_num)
   data =requests.get(url).text
   soup = bs.BeautifulSoup(data,'html.parser')
   tb = soup.find_all('div',{'class':'list_body newsflash_body'})

   headlines = []
   link_ed = []

   for i in tb:
      Raw = i.find_all('dt')

      for j in Raw:
         headlineRaw = j.find('a').text
         headlines.append(headlineRaw)

         link = j.find('a')
         link_ed.append(link.get('href'))

   links = []

   for link in link_ed:
      if link not in links:
         links.append(link)


   headlines_ed =[]

   for k in headlines:
      headlines_ed.append(k.strip())

   headlines = [x for x in headlines_ed if x.strip()]
   newspanel = pd.DataFrame(headlines)

   df = {'Headlines': headlines, 'links': links}
   print(pd.DataFrame(df))

naver_news()
