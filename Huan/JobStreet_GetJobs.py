# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 16:47:53 2019

@author: Admin

Scrape from JobStreet
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
listkey= ['data','data analyst','data engineer', 'data science', 'business analyst']
TechDetailed = namedtuple('TechDetailed', 'title, company, description')
start= time.time()
def detail(response):
    soup = bs(response.text, 'lxml')
    tit = soup.find('div', attrs={'class':'job_info'})
    if tit== None:
        return TechDetailed(title='', company='', description='')
    title = tit.select('h1')[0].text
#    print(title)
    cpm=soup.find('span', attrs = {'class':'company'})
    if cpm== None:
        company= 'Bài việt không đề cập tên Công ty'
    else:
        company = cpm.text
    description = soup.find('div', attrs={'class':'summary'}).text
    res=TechDetailed(title, company, description)
    return res
urls = []
for i in listkey:
    # type keyword and search
    print('BEGIN FIND JOBS with key: ',i)
    driver.get('https://www.jobstreet.vn/')
    keyword = driver.find_element_by_xpath("//input[@id='q']")
    keyword.clear()
    keyword.send_keys(i)
    keyword.send_keys(Keys.RETURN)
    xt= driver.find_elements_by_xpath("//div[@id='no_results']")
    if len(xt)>0:
#        print('    !!![WARNING]: not found any jobs with: "',i,'"!')
        continue
    count=0
    while True:
        count+=1
        if count==10:
            break
        
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
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
# Wait to load page-----------------------------------------------------------------------------------------------------------------------------------------------------------
        close=driver.find_elements_by_xpath("//div[@class='lean-overlay']")
        if(len(close))>0:
#            print("      !!![WARNING]:---have a fade in popup, wait a few second to close it before get the next page")
            time.sleep(1)
            driver.find_element_by_xpath("//div[@id='job_alert_modal']//a").click()
            time.sleep(1)
            
# all work will be here------------------------------------------------------------------------------------------
        source_code = driver.page_source    
        soup = bs(source_code, 'lxml')
        pre=soup.find('ul', attrs={'id':'jobresults'})
        jobs=pre.find_all('li', attrs={'class':'result'} )
        #       find element have link
        for item in jobs:
            base='https://jobstreet.vn'
            urlx=urljoin(base,item.select('a')[0]['href'] )
            urls.append(urlx)

#-------------------------------------------------------------------------------------------------------------  
        a=driver.find_elements_by_xpath("//a[@class='next_page']")
        if len(a)==0:
#            print("      no more job with this keyword, go to the next")
            break
#        print('     found ',len(a)," more jobs button in this page, click on it! ")
        a[0].click()
     
#    print('---Finish serach jobs with keyword: "',i,'"!')
#       use future sessssssssssion    
session = FuturesSession(max_workers=20)
futures = [session.get(url) for url in urls]
    
details = [detail(future.result()) for future in futures]
data_dict = {'url': urls, 'title': [detail.title for detail in details], 'company': [detail.company for detail in details], 'description':[detail.description for detail in details] }
data_frame = pd.DataFrame(data_dict)
end = time.time()
data_frame.to_csv('JobStreet.csv')
print(end - start)

