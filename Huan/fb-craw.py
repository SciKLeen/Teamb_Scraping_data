# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 16:47:53 2019

@author: Admin
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import timeit
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from collections import namedtuple
start= time.time()
SCROLL_PAUSE_TIME = 0.5
driver = webdriver.Chrome(r'C:\Users\Admin\Desktop\chromedriver.exe')
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
driver.get('https://www.facebook.com/groups/machinelearningcoban/')
while True:
    
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

source_code = driver.page_source    
soup = bs(source_code, 'lxml')

data = soup.find_all('div', attrs={'class':'_4-u2 mbm _4mrt _5jmm _5pat _5v3q _7cqq _4-u8'}) 



TechBasic = namedtuple('TechBasic', 'url, content, date, user')

def data_extraction(post):
    url_base = 'https://www.facebook.com'
    if len(post.select('p')) != 0:
        post_content =  post.select('p')[0].text
    else: 
        post_content = 0
    return TechBasic(url=urljoin(url_base, post.select('a')[0]['href']), content= post_content, date = post.select('abbr')[0]['title'], user = post.select('img')[0]['aria-label'])
    

results = []
for i in range(len(data)):
    results.append(data_extraction(data[i]))

#sau khi thu xong se sua 4 dong for nay lai 
urls_list = [results[i].url for i in range(len(data))]
content_list = [results[i].content for i in range(len(data))]
date_list = [results[i].date for i in range(len(data))]
user_list = [results[i].user for i in range(len(data))]

end=time.time()

time_elapse=end-start
#print( end - start)
#print(type(end))
#, 'time elapse':time-elapse
data_dict = {'URLs':urls_list, 'User':user_list, 'Content':content_list, 'Date':date_list , 'Time elapse':time_elapse}

data = pd.DataFrame(data_dict)

data.to_csv('machinelearningcoban.csv')
driver.quit()



