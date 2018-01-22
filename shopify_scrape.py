from selenium import webdriver
import time


def load_browser_loggin(user,password):
    '''  instantiates a webdriver called browser logged into shopify with the giver user, password
    INPUT: user, password both as strings
    OUTPUT: browser 
    '''
    browser = webdriver.Firefox()
    browser.get("https://drift-bikinis.myshopify.com/admin/")
    browser.find_element_by_id("Login").click()
    browser.find_element_by_id("Login").send_keys(user)
    browser.find_element_by_id("Password").click()
    browser.find_element_by_id("Password").send_keys(password)
    browser.find_element_by_id("LoginSubmit").click()
    return browser
    
def scrape_visitor_info(start_yr, end_yr, start_month, end_month, start_day, end_day): 
    '''
    INPUT: start and end dates (includive) to scrape visitor info for. all as integers
    OUTPUT: visitors- list of lists of lists. each sublist consists of the folowing lists:
                      [date],[type of source, source, # of visitors, # of sessions]. This final element 
                      is repeated for each unique source.  
    '''
    visitors = []
    for year in range(start_yr,end_yr+1):
        for month in range(start_month,end_month+1):
            if month < 10:
                month = '0{}'.format(month)
            for day in range(start_day,end_day+1):
                if day < 10:
                    day = '0{}'.format(day)
                date = '{}-{}-{}'.format(year,month,day)
                if day == 31 and month in ['02','04', '06', '09', 11]:
                    break
                elif day in [29,30] and month == '02':
                    break
                date_info = [[date]]
                print(date)
                browser.get('https://drift-bikinis.myshopify.com/admin/reports/visitors_by_referrer?startDate={}&endDate={}'.format(date, date))
                if browser.find_elements_by_class_name('ui-data-table__row'):    
                    info = browser.find_elements_by_class_name('ui-data-table__row')
                    for item in info:
                        date_info.append((item.text).split())
                visitors.append(date_info)
                time.sleep(2)
    for item in visitors:
        item.remove(item[1])            
    return visitors

def convert_data(data_list):
    ''' Converts output of scrape_visitor_info() to a dictionary
    INPUT: data_list - list of lists of lists (output from scrape_visitor_info() )
    OUTPUT : date_traffic : Dictionary with dates as keys, dictionaries as values. value keys are
            source types, value values are (number of visitors, number of sessions).
    '''
    date_traffic={}
    for item in data_list:
        data = {}
        for i in range(1,len(item)):
            if item[i][0]=='Direct':
                data[item[i][0]]=(item[i][2],item[i][3])
            elif item[i][0]=='Social':
                data[item[i][1]]=(item[i][2],item[i][3])
            elif item[i][0]=='Search':
                data['Search/'+item[i][1]]=(item[i][2],item[i][3])
            elif len(item[i]) == 4:
                data[item[i][0]+item[i][1]]=(item[i][2],item[i][3])
            else:
                data[item[i][0]]= ([item[i][n] for n in range(1, len(item[i]))])
        date_traffic[item[0][0]] = data
    return date_traffic  