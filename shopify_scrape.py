from selenium import webdriver
import time
import math


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
    
def scrape_visitor_info(browser,start_yr, end_yr, start_month, end_month, start_day, end_day): 
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
                time.sleep(2)
                if browser.find_elements_by_class_name('ui-data-table__row') != []:    
                    info = browser.find_elements_by_class_name('ui-data-table__row')
                    for item in info:
                        date_info.append((item.text).split())
                date_info.remove(['Referrer', 'source', 'Referrer', 'name', 'Visitors', 'Sessions'])
                visitors.append(date_info)
                time.sleep(2)           
    return visitors

def scrape_orders(browser, orders_to_scrape):
    '''
    INPUT:
          browser - webdriver signed into shopify (use load_browser_loggin() )
          orders_to_scrape - int, how many orders from the most recent order to scrape
    
    '''
    url = 'https://drift-bikinis.myshopify.com/admin/orders'
    browser.get(url)
    order_info = []
    pages = math.ceil(orders_to_scrape/50)
    on_last_page = orders_to_scrape - ((pages - 1) * 50)
    while pages > 1 : 
        for i in range(50):
            orders = browser.find_elements_by_class_name('ui-nested-link-container')
            orders[47+i].click()
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
        orders[i].click()
        time.sleep(2)
        info = scrape_order_info(browser)
        order_info.append(info)
        browser.get(url)
        time.sleep(2)
    return order_info
    
    
    
    
def scrape_order_info(browser):
    info = []
    items = browser.find_elements_by_class_name('orders-line-item')
    for i in range(len(items)):
        item = items[i]
        item_description = item.find_element_by_class_name('orders-line-item__description').text
        item_price = item.find_element_by_class_name('orders-line-item__price').text
        info.append((item_description, item_price))
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










