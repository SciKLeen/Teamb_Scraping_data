# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:42:59 2019

@author: Admin

From Nuah with Coursera.org
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
#listkey=['https://www.coursera.org/courses?query=data%20science&refinementList%5Blanguage%5D%5B0%5D=English&page=1&configure%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BhitsPerPage%5D=7&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BhitsPerPage%5D=4&indices%5Btest_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true']
listkey= ['https://www.coursera.org/courses?query=data%20science&refinementList%5Blanguage%5D%5B0%5D=English&page=1&configure%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BhitsPerPage%5D=7&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BhitsPerPage%5D=4&indices%5Btest_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true','https://www.coursera.org/courses?query=data%20analysis&refinementList%5Blanguage%5D%5B0%5D=English&page=1&configure%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BhitsPerPage%5D=7&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BhitsPerPage%5D=4&indices%5Btest_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true', 'https://www.coursera.org/courses?query=data%20engineering&page=1&configure%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_suggestions%5D%5Bconfigure%5D%5BhitsPerPage%5D=7&indices%5Btest_suggestions%5D%5BrefinementList%5D%5Bpage%5D=1&indices%5Btest_suggestions%5D%5Bpage%5D=1&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_degrees_keyword_only%5D%5Bconfigure%5D%5BhitsPerPage%5D=4&indices%5Btest_degrees_keyword_only%5D%5BrefinementList%5D%5Bpage%5D=1&indices%5Btest_degrees_keyword_only%5D%5Bpage%5D=1&indices%5Btest_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Btest_products%5D%5BrefinementList%5D%5Bpage%5D=1&indices%5Btest_products%5D%5Bpage%5D=1&refinementList%5Blanguage%5D%5B0%5D=English']
CourseDetailed = namedtuple('CourseDetailed', 'title, company, description')
start= time.time()
def detail(response):
#    time.sleep(2)
    soup = bs(response.text, 'lxml')
#    print(response)
    tit = soup.find('div', attrs={'class':'content bt3-col-xs-12 bt3-col-sm-12 bt3-col-md-12 bt3-col-lg-12'})
    if tit== None:
        tit = soup.find('h1', attrs={'class':'H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s'})
        if tit==None :
            tit = soup.find('h2', attrs={'class':'display-5-text degree-name'})
            if tit== None:
                title='Degrees & Certificates'
                print(title)
#            print(response)
            else:
                title= tit.text
        else:
            title = tit.text
#            print('tit nay tu h1')
    else:
        title = tit.text
#        print('tit nay tu h2')
#    print(title)

    company = 'Empty()'
    des = soup.find('div', attrs={'class':'AboutCourse'})
    if des== None:
        des=soup.find('div', attrs={'class':'rc-Column bt3-col-xs-12 bt3-col-md-7 rc-MainColumn'})
        if des==None:
            des=soup.find('div',attrs={'class':'content-inner'})
            if des==None:
                des='Degrees & Certificates'
            else:
                des=des.text
        else:
            des=des.find('div')
            des=des.text
    else :
        des=des.text
    
    res=CourseDetailed(title, company, des)
    return res
urls = []
for i in listkey:
    driver.get(i)
#    source_code = driver.page_source    
#    soup = bs(source_code, 'lxml')
    while True:
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for scr in range(100):
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(0.7)
                a=driver.find_elements_by_class_name('ais-InfiniteHits-loadMore')
#                print('-111111111111111111111111111',len(a))
                if len(a)==0:
#                    print("      no more job with this keyword, go to the next")
                    break
        #        print('     found ',len(a)," more jobs button in this page, click on it! ")
                for cl in a:
                    cl.click()
#                a[-1].click()
            #-------------------------------------------------------------------------------------------------------------  
#        time.sleep(100)
# Wait to load page-----------------------------------------------------------------------------------------------------------------------------------------------------------
#        close=driver.find_elements_by_xpath("//div[@class='lean-overlay']")
#        if(len(close))>0:
##            print("      !!![WARNING]:---have a fade in popup, wait a few second to close it before get the next page")
#            time.sleep(1)
#            driver.find_element_by_xpath("//div[@id='job_alert_modal']//a").click()
#            time.sleep(1)
#            
# all work will be here------------------------------------------------------------------------------------------
        source_code = driver.page_source    
        soup = bs(source_code, 'lxml')
#        pre=soup.find('ul', attrs={'id':'jobresults'})
        jobs=soup.find_all('li', attrs={'class':'ais-InfiniteHits-item'} )
        print(len(jobs))
        #       find element have link
        for item in jobs:
            base='https://coursera.org'
            urlx=urljoin(base,item.select('a')[0]['href'] )
            urls.append(urlx)
            print(urlx)
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
data_frame.to_csv('COURSERA-ORG.csv')
print(end - start)

