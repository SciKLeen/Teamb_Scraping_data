import time
import pandas

from selenium                       import webdriver
from selenium.webdriver.common.keys import Keys
from pandas                         import ExcelWriter
from bs4                            import BeautifulSoup as bs

key_words = ['data science', 'data analyst', 'data engineer', 'business analyst', 'business intelligence'];

#Object
tittle = [];
view = [];
category = [];
job_type = [];
address = [];
From  = [];
To = [];
content = [];

#get time prg run
#a_struct_time = time.localtime();
#ticks = time.mktime(a_struct_time);

driver = webdriver.Chrome(r"C:\WebDrivers\chromedriver.exe");

#---------------------------------------------------------------
for str in key_words: 
    driver.get('https://www.internship.edu.vn');
    input_keyword = driver.find_element_by_class_name('form-control');
    input_keyword.clear();
    input_keyword.send_keys(str);
    input_keyword.send_keys(Keys.RETURN);
    
    time.sleep(2);
    while(1):
        Height = driver.execute_script("return document.body.scrollHeight");
        
        while( len(driver.find_elements_by_xpath('//div[@style = "opacity: 1; display: none;"]')) == 0):
            driver.find_elements_by_xpath('//div[@class = "loadmore-action"]')[0].click();
            time.sleep(2);

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
        
        new_height = driver.execute_script("return document.body.scrollHeight");
        if(new_height == Height):
            break;
            

    
#   get Source
    html_doc = driver.page_source;
    soup = bs(html_doc,'html.parser');

        
        
#   lAY SO LUONG BAI POST
    #Find =        soup.find_all('div', attrs = {'Class': 'jobs posts-loop'});
    post_count = int(soup.find_all('span', attrs={'class': 'text-primary'})[0].text); #Find (at most) *one*
    
#   get link
    parent_divs = soup.find_all('div', attrs={'Class': 'jobs posts-loop '}); #Find (at most) *one*
    child_divs = soup.find_all('div', attrs={'class': 'show-view-more'});
     
    for item in range(0, post_count, 1):
        link = child_divs[item].find('a');
        driver.get(link['href']);
        time.sleep(2);
         
        little_html_doc = driver.page_source;    
        little_soup = bs(little_html_doc,'html.parser');
         

        #get content
        #get view
        t_view = little_soup.find('span', attrs = {'class': 'count'});
        if(t_view != None):  
            t_view = t_view.text;
            t_view_len = len(t_view);
            # xxx lượt xem -> xxx
            t_view = t_view[ : t_view_len - 9];
        else:
                t_view = 'NaH'
            
         
        #Get title
        t_tittle = little_soup.find('h1', attrs = {'class': 'page-title'});
        if(t_tittle != None):
            t_tittle = t_tittle.text;
            t_tittle_len = len(t_tittle);
            t_tittle = t_tittle[ : t_tittle_len - t_view_len - 1];
        else:
            t_tittle = 'NaH'
            
        #Get job type
        t_Jobtype_span = little_soup.find('span', attrs = {'class': 'job-type'});
        if(t_Jobtype_span != None):
            i_tag = t_Jobtype_span.find('i').text;
            t_Jobtype = (t_Jobtype_span.text)[len(i_tag) : ];
        else:
            t_Jobtype = 'Nah';
                 
        #get address
        t_address_span = little_soup.find('span', attrs = {'class': 'job-location'});
        if(t_address_span != None):    
            t_address = t_address_span.find('a').text;
        else:
            t_address = 'Nah';
        
        #get Categorys
        job_category_span = little_soup.find('span', attrs = {'class': 'job-category'}); #get tab bar (Job, address, topic)
        if(job_category_span != None):
            lst_category = job_category_span.find_all('a');
            t_Categorys = '';
            for cat in lst_category:
                t_Categorys += (cat.text + '-');
            t_Categorys = t_Categorys[ : len(t_Categorys) - 1];
        else:
            t_Categorys = 'Nah';
        
        #get time bar
        Durection_bar = little_soup.find('time', attrs = {'class': 'entry-date'});
        Durection = Durection_bar.find_all('span');      
        if(len(Durection) == 2):
            t_from = Durection[0].text;
            t_to = Durection[1].text;
            t_to = t_to[3 : ];
        else:
            if(len(Durection) == 1):
                t_from = Durection[0].text;
                t_to = 'NaH'
            else:
                t_from = 'NaH';
                t_to = 'NaH'
        
        #get content
        t_content = little_soup.find('div', attrs = {'class', 'job-desc'}).text;
        
         
         
         
        tittle.append(t_tittle);
        view.append(t_view);
        job_type.append(t_Jobtype);
        address.append(t_address);
        category.append(t_Categorys);
        From.append(t_from);
        To.append(t_to);
        content.append(t_content);

#n = len(tittle);
#for i in (0, n, 1):
#    for j in (i + 1, len(tittle), 1):
#        if(tittle[i][0] == tittle[j][0]):
#            tittle.pop(j);
#            view.pop(j);
#            category.pop(j);
#            job_type.pop(j);
#            address.pop(j);
#            From.pop(j);
#            To.pop(j);
#            content.pop(j);
#            
#            n -= 1;
#            
    
    
#write to excel
df = pandas.DataFrame({'Title':     tittle, 
                       'View':      view,
                       'Job type':  job_type,
                       'Address':   address,
                       'Category':  category,
                       'From':      From,
                       'To':        To,
                       'Content':   content
                       });

writer = ExcelWriter("doc/internship.xlsx");
df.to_excel(writer);
writer.save();

#ticks = (time.mktime(time.localtime()) - ticks) / 60.0;
#print(ticks);
#
print('End');

