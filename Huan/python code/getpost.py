# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:47:53 2019

@author: Admin

Scrape from ITviecs
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import timeit
import time
import pandas as pd
from pandas import ExcelWriter
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from collections import namedtuple
start= time.time()
driver = webdriver.Chrome(r'C:\Users\Admin\Desktop\chromedriver.exe')
driver2 = webdriver.Chrome(r'C:\Users\Admin\Desktop\chromedriver.exe')
last_height = driver.execute_script("return document.body.scrollHeight")
driver.get('https://careerbuilder.vn/viec-lam/data-k-vi.html')

count=0
source_code = driver.page_source    
soup = bs(source_code, 'lxml')
data = soup.find_all('div', attrs={'class':'gird_standard'}) 
# tên cong ty
# vị trí công việc tuyển
# địa chỉ
# yêu cầu
ans = namedtuple('ans', 'com,pos,add,req,url')
while True:
    
    # Scroll down to bottom
    Adriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
#    data = soup.find_all('div', attrs={'class':'gird_standard'})
#    dtx= data.
    
    
    
    
    xt=driver.find_elements_by_link_text("Trang kế tiếp")
    if len(xt) == 0:
        break
    xt.click()
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(10)

driver2 = webdriver.Chrome(r'C:\Users\Admin\Desktop\chromedriver.exe')
def sol(post):
    url_base = 'https://itviec.com'
    url=urljoin(url_base, post.select('a')[0]['href'])
#    print(post.select('a')[0]['href'])
    
    driver2.get(url)
    source = driver2.page_source    
    soup = bs(source, 'lxml')
#    get company name
    jobdetails = soup.find_all('div', attrs={'class':'employer-info'})
    jobdetail=jobdetails[0];
    post_com=jobdetail.select('a')[0].text
#    get address & position
    poss = soup.find_all('h1', attrs={'class':'job_title'})
    post_pos=poss[0].text
    addrs = soup.find_all('div', attrs={'class':'address__full-address'})
    post_add= addrs[0].text
    
#    get link post
    post_url= url
    
#   get requirement
    reqs= soup.find_all('div', attrs={'class':'experience'})
    post_req=reqs[0].text
    return ans(com = post_com, pos = post_pos,add = post_add,req = post_req,url = post_url)
results = []
com_list = []
pos_list = []
url_list = []
req_list = []
add_list = []
for i in range(len(data)):
    results.append(sol(data[i]))
for i in range (len(data)):
    com_list.append(results[i].com)
    pos_list.append(results[i].pos)
    url_list.append(results[i].url)
    req_list.append(results[i].req)
    add_list.append(results[i].add)

end=time.time()

time_elapse=end-start
df = pd.DataFrame({'Company':com_list, 
                   'Position':pos_list, 
                   'Address':add_list ,
                   'Requirement':req_list, 
                   'Url':url_list,
                   'Time elapse':time_elapse
                   })
writer = ExcelWriter("ITviec_RevolveS.xlsx")
df.to_excel(writer)
writer.save()
driver.quit()



