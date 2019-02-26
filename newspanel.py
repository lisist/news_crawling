import pandas as pd
import bs4 as bs
import requests
import os
import warnings
import datetime as dt

warnings.simplefilter(action='ignore', category=FutureWarning)

def newspanel(pageNum_max=2) :

   headlines = []
   links = []


   for pagenum in range(1,pageNum_max+1):

      url = 'http://news.einfomax.co.kr/news/articleList.html?page='+str(pagenum)+'&sc_section_code=S1N4'
      data = requests.get(url).text

      soup = bs.BeautifulSoup(data,"html.parser")

      tb = soup.find_all('div',{'class':'list-titles table-cell'})

      for i in tb[:tb.__len__()-1]:
         headlineRaw = i.find('a').text
         headlines.append(headlineRaw)

         link = i.find('a')
         links.append(link.get('href'))

   df = {'Headlines':headlines,'links':links}
   newspanel = pd.DataFrame(df)
   newspanel.dropna(inplace=True)
   newspanel.to_csv('newsdata.csv',index=False)

   print("New News updated\n")


def show_headlines():
   df = pd.read_csv('newsdata.csv')
   headlinesDF = df['Headlines']
   headlinesDF.to_csv('news_headlines.csv',index=True)
   print(df['Headlines'])

def ni(index_num=1):
   df = pd.read_csv('newsdata.csv')
   links = list(df['links'])
   link = links[index_num]

   url_for_content = 'http://news.einfomax.co.kr'+link

   newsContent_raw = requests.get(url_for_content).text
   content_soup = bs.BeautifulSoup(newsContent_raw,"html.parser")

   table = content_soup.find('div',{'id':'article-view-content-div'})

   content = table.text
   content = content.replace('\t','')
   content = content.replace('\r','')
   content = content.replace('\n\n\n\n','')

   print('\n')
   print(content)

   ## bookmarking already read news

   BookmarkHeadline_list = list(df['Headlines'])
   BookmarkHeadline = BookmarkHeadline_list[index_num]

   now = dt.datetime.now()
   Bookmarkdate = str(now)[0:10]
   BookmarkDic = {"Headlines":[BookmarkHeadline],"Date":[Bookmarkdate],"Links":[link]}
   BookmarkDataFrame = pd.DataFrame(BookmarkDic)


   if not os.path.exists('news_bookmark.csv'):
      BookmarkDataFrame.to_csv('news_bookmark.csv',index=False)
   else:
      BookmarkDF_prior = pd.read_csv('news_bookmark.csv')
      link_prior = BookmarkDF_prior['Links']
      headlines_priror = BookmarkDF_prior['Headlines']

      current = [BookmarkHeadline, Bookmarkdate, link]
      BookmarkDF_prior.loc[len(BookmarkDF_prior),:] = current

      BookmarkDF_prior.to_csv('news_bookmark.csv',index=False)

def shell():
   os.system('cls')
   while True:
      a = input("> ")

      if (a == 'q'):
         break
      elif (a == 'news'):
         newspanel(2)
      elif (a == 'headlines'):
         show_headlines()
         k = 0
         while True:
            a = input('headlines > articles > ')
            if (a == 'headlines'):
               show_headlines()
            elif (a == 'back'):
               break
            elif (a == 'n'):
               ni(int(k) + 1)
               k = k + 1
            elif (a == 'b'):
               if (k == 0):
                  k = 1
               ni(int(k) - 1)
               k = k - 1

            else:
               try:
                  ni(int(a))
                  k = int(a)
               except:
                  True

shell()
