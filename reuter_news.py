import pandas as pd
import bs4 as bs
import requests
import warnings
import datetime as dt

warnings.simplefilter(action='ignore', category=FutureWarning)

def reuter_news():

   url = 'https://www.reuters.com/finance/markets'
   data =requests.get(url).text
   soup = bs.BeautifulSoup(data,'html.parser')

   tb = soup.find_all('div',{'class':'moduleBody'})

   headlines =[]
   link_ed = []

   for i in tb:
      headlinesRaw = i.find_all('a')
      for j in headlinesRaw:
         headlines.append(j.text)

         link_ed.append(j.get('href'))

   headlines = [x for x in headlines if x.strip()]
   print(headlines)

   links =[]
   for link in link_ed:
      if link not in links and link[0:8] == '/article':
         links.append(link)

   df = {'Headlines':headlines,'links':links}
   print(pd.DataFrame(df))



reuter_news()
