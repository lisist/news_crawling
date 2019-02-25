import pandas as pd
import bs4 as bs
import requests
import os
import csv

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

   BookmarkHeadline = content[20:100]
   BookmarkHeadline = BookmarkHeadline.replace('\n','')

   BookmarkDic = {"Links":[link],"Headlines":[BookmarkHeadline]}
   BookmarkDataFrame = pd.DataFrame(BookmarkDic)


   if not os.path.exists('news_bookmark.csv'):
      BookmarkDataFrame.to_csv('news_bookmark.csv',index=False)
   else:
      BookmarkDF_prior = pd.read_csv('news_bookmark.csv')
      link_prior = BookmarkDF_prior['Links']
      headlines_priror = BookmarkDF_prior['Headlines']

      current = [link, BookmarkHeadline]
      BookmarkDF_prior.loc[len(BookmarkDF_prior),:] = current

      BookmarkDF_prior.to_csv('news_bookmark.csv',index=False)


while True:
   print('\n-----------------------------------------')
   print('1. Newscawling (type : news)             ')
   print('2. Show headlines (type : headlines)     ')
   print('3. Show content (type ni(숫자)           ')
   print('4. Quit (type q)                         ')
   print('-----------------------------------------')
   a = input("which : ")
   print('\n')

   if (a=='q'):
      break
   elif (a=='news'):
      newspanel(2)
   elif (a=='headlines'):
      show_headlines()
      print('------------------------------------------')
      print('want to back to headlines (type headlines)')
      print('------------------------------------------')
      a = input('which articles : ')
      if (a=='headlines'):
         headlines()
      else:
         ni(int(a))
