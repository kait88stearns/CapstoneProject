from selenium import webdriver
import time
import math
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re


def load_browser_loggin(user,password):
    '''  
    INPUT: user - shopify username 
           password - shopify password
    OUTPUT: browser - webdriver logged into shopify sith given credentials   
    '''
    #dcap = webdriver.DesiredCapabilities.PHANTOMJS
    #dcap["phantomjs.page.settings.userAgent"] = (
    #'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20120815 Firefox/16.0' )
    #browser = webdriver.PhantomJS(desired_capabilities=dcap)
    #browser.set_window_size(1120, 550)
    browser = webdriver.Firefox()
    browser.get("https://drift-bikinis.myshopify.com/admin/")
    browser.find_element_by_id("Login").click()
    browser.find_element_by_id("Login").send_keys(user)
    browser.find_element_by_id("Password").click()
    browser.find_element_by_id("Password").send_keys(password)
    browser.find_element_by_id("LoginSubmit").click()
    return browser
    
def scrape_visitor_info(browser,start_yr, end_yr, start_month, end_month, start_day, end_day): 
    '''
    INPUT: start and end dates(inclusive). all as integers
    OUTPUT: visitors - list of lists of lists.  
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
                time.sleep(2)
                if browser.find_elements_by_class_name('ui-data-table__row') != []:    
                    info = browser.find_elements_by_class_name('ui-data-table__row')
                    for item in info:
                        date_info.append((item.text).split())
                date_info.remove(['Referrer', 'source', 'Referrer', 'name', 'Visitors', 'Sessions'])
                visitors.append(date_info)
                time.sleep(2)           
    return visitors



def scrape_orders(browser, orders_to_scrape, path_to_csv,init_url='https://drift-bikinis.myshopify.com/admin/orders'):
    ''' scrapes orders, writes to csv
    INPUT:
          browser - webdriver signed into shopify (use load_browser_loggin() )
          orders_to_scrape - int, how many orders from most recent order to scrape   
    '''
    url = init_url
    browser.get(url)
    order_info = []
    pages = math.ceil(orders_to_scrape/50)
    on_last_page = orders_to_scrape - ((pages - 1) * 50)
    while pages > 1 : 
        for i in range(50):
            orders = browser.find_elements_by_class_name('ui-nested-link-container')
            orders[i].click()
            time.sleep(2)
            info = scrape_order_info(browser)
            order_info.append(info)
            browser.get(url)
            time.sleep(2)
        pages -= 1    
        next_page = browser.find_element_by_id("pagination-links").find_elements_by_tag_name('li')[1]
        url = next_page.find_element_by_tag_name('a').get_attribute('href')
        next_page.click()
        time.sleep(3)
    for i in range(on_last_page):
        orders = browser.find_elements_by_class_name('ui-nested-link-container')
        print(orders)
        orders[i].click()
        time.sleep(2)
        info = scrape_order_info(browser)
        order_info.append(info)
        browser.get(url)
        time.sleep(2)    
    df = pd.DataFrame(order_info, columns=['items', 'total', 'sale_time', 'order_num','customer', 'pos'])
    df.to_csv(path_to_csv) 
    return url
    
    
def scrape_order_info(browser):
    info = []
    items = browser.find_elements_by_class_name('orders-line-item')
    items_desc = []
    for i in range(len(items)):
        item = items[i]
        item_description = item.find_element_by_class_name('orders-line-item__description').text
        item_price = item.find_element_by_class_name('orders-line-item__price').text
        items_desc.append((item_description, item_price))
    info.append(items_desc)
    checkout = browser.find_element_by_id('transaction_summary')
    total = checkout.find_elements_by_tag_name('strong')[1].text    
    info.append(total)
    order_date_pointer = browser.find_elements_by_class_name('ui-title-bar__metadata')
    order_date = order_date_pointer[0].text
    info.append(order_date)
    order_num_pointer = browser.find_elements_by_class_name('ui-title-bar__title')
    order_num = order_num_pointer[0].text
    info.append(order_num)
    customer_info = browser.find_element_by_id('customer-card')
    customer_sections = customer_info.find_elements_by_class_name('ui-card__section')
    if customer_sections[0].find_elements_by_tag_name('a') != []:
        customer_name = customer_sections[0].find_element_by_tag_name('a').text
    else:    
        customer_name = 'NA'
    info.append(customer_name)    
    sales_info = browser.find_element_by_id('order_card')
    pos_details =sales_info.find_element_by_class_name('ui-card__header')
    pos = pos_details.find_element_by_tag_name('p').text  
    info.append(pos)
    return info


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
                data[item[i][0]] = ([item[i][n] for n in range(1, len(item[i]))])
        date_traffic[item[0][0]] = data
    return date_traffic  


def webtraffic_csv_to_cleandf(csv_path):
    ''' 
    INPUT: path to csv of webtraffic data
    OUTPUT: properly formatted dataframe
    '''
    df = pd.read_csv(csv_path)
    df.fillna(0, inplace=True)
    traffic_dict = df.to_dict(orient='list')
    new_dict = reformat_dictionary(traffic_dict)
    df = pd.DataFrame(new_dict)
    df = df.transpose()
    return df

def reformat_dictionary(traffic_dict):
    '''
    used in web_traffic_csv_to_cleandf()
    '''
    
    sources = traffic_dict['Unnamed: 0'] 
    new_traffic_dict = {}
    for key, val in traffic_dict.items():
        if key != 'Unnamed: 0':
            new_val = []
            for item in val:
                if type(item) == str and item not in sources:
                    matches = re.findall('\d+' , item)
                    new_val.append((int(matches[0]), int(matches[1])))
                else:
                    new_val.append(item)
            new_val_dict = {}
            new_val_dict['Direct'] = 0
            new_val_dict['Email'] = 0
            new_val_dict['Facebook'] = 0
            new_val_dict['Iconosquare'] = 0
            new_val_dict['Instagram'] = 0
            new_val_dict['Pintrest'] = 0
            new_val_dict['Search'] = 0
            new_val_dict['Unknown'] = 0
            if type(new_val[0]) == tuple:
                new_val_dict['Direct'] += new_val[0][0]    
            for i in range(1, 4):
                if type(new_val[i]) == tuple:
                    new_val_dict['Email'] += new_val[i][0]
            if type(new_val[4]) == tuple:
                new_val_dict['Facebook'] += new_val[4][0]   
            if type(new_val[5]) == tuple:
                new_val_dict['Iconosquare'] += new_val[5][0]
            if type(new_val[6]) == tuple:
                new_val_dict['Instagram'] += new_val[6][0]
            if type(new_val[7]) == tuple:
                new_val_dict['Pintrest'] += new_val[7][0]
            for i in range(8, 19):
                if type(new_val[i]) == tuple:
                    new_val_dict['Search'] = new_val[i][0]
            if type(new_val[19]) == tuple:
                new_val_dict['Unknown'] += new_val[19][0]        
            new_traffic_dict[key] = new_val_dict  
    return new_traffic_dict 






