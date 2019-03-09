# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:19:53 2019

@author: Admin - edx.org
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import timeit
import time
import pandas as pd
from pandas import ExcelWriter
from bs4 import BeautifulSoup as bs
from collections import namedtuple
from requests_futures.sessions import FuturesSession
from urllib.parse import urljoin

driver = webdriver.Chrome(r'C:\Users\Admin\Desktop\chromedriver.exe')
listkey= ['https://www.edx.org/course/?search_query=data%20science']
CourseDetailed = namedtuple('CourseDetailed', 'title, company, description')
start= time.time()
def detail(response):
    soup = bs(response.text, 'lxml')
    tit = soup.find('div', attrs={'class':'job_info'})
    if tit== None:
        return CourseDetailed(title='', company='', description='')
    title = tit.select('h1')[0].text
#    print(title)
    cpm=soup.find('span', attrs = {'class':'company'})
    if cpm== None:
        company= 'Bài việt không đề cập tên trung tâm'
    else:
        company = cpm.text
    description = soup.find('div', attrs={'class':'summary'}).text
    res=CourseDetailed(title, company, description)
    return res
urls = []
for i in listkey:
    driver.get(i)
#    source_code = driver.page_source    
#    soup = bs(source_code, 'lxml')
#    while True:
#        SCROLL_PAUSE_TIME = 0.5
#
#        # Get scroll height
#        last_height = driver.execute_script("return document.body.scrollHeight")
#        while True:
#            # Scroll down to bottom
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#        
#            # Wait to load page
#            time.sleep(SCROLL_PAUSE_TIME)
#        
#            # Calculate new scroll height and compare with last scroll height
#            new_height = driver.execute_script("return document.body.scrollHeight")
#            if new_height == last_height:
#                break
#            last_height = new_height
# all work will be here------------------------------------------------------------------------------------------
        source_code = driver.page_source    
        soup = bs(source_code, 'lxml')
#        pre=soup.find('ul', attrs={'id':'jobresults'})
        jobs=soup.find_all('div', attrs={'class':'course-card'} )
        print(len(jobs))
        #       find element have link
        for item in jobs:
            base='https://edx.org'
            urlx=urljoin(base,item.select('a')[0]['href'] )
            urls.append(urlx)
#            print(urlx)
        break

     
#    print('---Finish serach jobs with keyword: "',i,'"!')
#       use future sessssssssssion
print('here')
session = FuturesSession(max_workers=20)
futures = [session.get(url) for url in urls]
    
details = [detail(future.result()) for future in futures]
data_dict = {'url': urls, 'title': [detail.title for detail in details], 'company': [detail.company for detail in details], 'description':[detail.description for detail in details] }
data_frame = pd.DataFrame(data_dict)
end = time.time()
data_frame.to_csv('edx-ORG.csv')
print(end - start)