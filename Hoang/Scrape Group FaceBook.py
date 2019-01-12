import time
#import pandas

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import ExcelWriter
from bs4 import BeautifulSoup as bs

Ids = [];
CtnS = [];
index = 10;

#get time now
a_struct_time = time.localtime();
ticks = time.mktime(a_struct_time);

driver = webdriver.Chrome(r"C:\WebDrivers\chromedriver.exe");

#load Page
Height = driver.execute_script("return document.body.scrollHeight");
driver.get('https://www.facebook.com/groups/277136939391233/');

print('Load page is succeeded, scroll page');

#scroll page
while 1:
    index = index - 1;
    #scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
    
    #wait to load page
    time.sleep(1);
    
    #get new height
    newHeight = driver.execute_script("return document.body.scrollHeight");
    
    if(newHeight == Height):
        print('~~~~~~~~~~~~~~~~~Stop Scroll~~~~~~~~~~~~~~~~');
        break;
        
    Height = newHeight;

#get Source
html_doc = driver.page_source;    
soup = bs(html_doc,'html.parser');

#get post
parent_div = soup.find_all('div', attrs={'class': '_4-u2 mbm _4mrt _5jmm _5pat _5v3q _7cqq _4-u8'}) #Find (at most) *one*
#print(parent_div)

#Get content
size = len(parent_div);
for i in range (0, size, 1):
    test = parent_div[i].select('p');
    
    Ids.append(i + 1);
    
    size_p = len(test);
    Str = '';
    for j in range (0, size_p, 1):
        Str = Str + '\n' + test[j].text;
    if(Str == ''):
        Str = '0';
    CtnS.append(Str);
    
ticks = (time.mktime(time.localtime()) - ticks) / 60.0;
print(ticks);

#write to excel
df = pandas.DataFrame({'Index':Ids, 'Content':CtnS});

writer = ExcelWriter("doc/Business_Analytics_&_Decision_Making_Community.xlsx");
df.to_excel(writer);
writer.save();

print('End');
