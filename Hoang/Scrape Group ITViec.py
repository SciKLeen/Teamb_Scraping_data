import time
import pandas

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import ExcelWriter
from bs4 import BeautifulSoup as bs

#Object
Ids = [];
company_name = [];
company_info = [];
Staff_count = [];
country = [];
working_time= [];
OT = [];
link = [];

Job = [];
language_youNeed = [];
address = [];

#get time prg run
a_struct_time = time.localtime();
ticks = time.mktime(a_struct_time);

driver = webdriver.Chrome(r"C:\WebDrivers\chromedriver.exe");

#load Page
Height = driver.execute_script("return document.body.scrollHeight");
driver.get('https://www.internship.edu.vn/?post_type=noo_job&s=data+engineering&location=&category=');

print('Load page is succeeded, scroll page');


#get Source
html_doc = driver.page_source;    
soup = bs(html_doc,'html.parser');

#get post
parent_divs = soup.find_all('div', attrs={'class': 'loadmore-wrap'}); #Find (at most) *one*
child_divs = soup.find_all('div', attrs={'class': 'show-view-more'});

for item in child_divs:
     link = item.find('a');
     print(link);
     
#for i in range(0, Len, 1):
#    print(article[i].get('href'));
