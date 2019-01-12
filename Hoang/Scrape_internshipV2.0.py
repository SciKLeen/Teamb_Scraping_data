import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import ExcelWriter
from bs4 import BeautifulSoup as bs

key_words = ('data scientist');

#Object
title = [];
From  = [];
To = [];
content = [];

#get time prg run
a_struct_time = time.localtime();
ticks = time.mktime(a_struct_time);

# get chromedriver dir
driver = webdriver.Chrome(r"..\chromedriver.exe");

#---------------------------------------------------------------
for str in key_words: 
    driver.get('https://www.internship.edu.vn/');
    input_keyword = driver.find_element_by_class_name('form-control');
    input_keyword.clear();
    input_keyword.send_keys(str);
    input_keyword.send_keys(Keys.RETURN);
    #get Source
    html_doc = driver.page_source;
    soup = bs(html_doc,'html.parser');
    
    #get post
    parent_divs = soup.find_all('div', attrs={'class': 'loadmore-wrap'}); #Find (at most) *one*
    child_divs = soup.find_all('div', attrs={'class': 'show-view-more'});
    
    for item in child_divs:
         link = item.find('a');
         driver.get(link['href']);
         
         little_html_doc = driver.page_source;    
         little_soup = bs(little_html_doc,'html.parser');
         
         #get content
         title.append(little_soup.find('h1', attrs={'class':'page-title'}).text);
         
         Time = little_soup.find('time', attrs={'class':'entry-date'});
         From_To = Time.find_all('span');
         From.append(From_To[0].text);
         To.append(From_To[1].text);
         
         content.append(little_soup.find('div', attrs={'job-desc'}).text);
#--------------------------------------------------------------
        
#write to excel
df = pandas.DataFrame({'Title':title, 
                       'From':From,
                       'To':To,
                       'Content': content});

writer = ExcelWriter("doc/internship.xlsx");
df.to_excel(writer);
writer.save();

ticks = (time.mktime(time.localtime()) - ticks) / 60.0;
print(ticks);

print('End');



