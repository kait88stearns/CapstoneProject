import numpy as np
import re 
from selenium import webdriver
import time 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
import pickle



def login_insta(user, password):
    '''
    INPUT: user, password
    OUTPUT: browser - headless firefox browser logged into instagram
    '''
    
    options = Options()
    options.add_argument('-headless')
    browser = Firefox(executable_path='geckodriver', firefox_options=options)
    time.sleep(3)
    # log into insta and go to profile
    browser.get("https://www.instagram.com/")
    time.sleep(2)
    browser.find_elements_by_class_name('_f9sjj')[1].find_element_by_tag_name('a').click()
    time.sleep(2)
    #browser.find_element_by_class_name('_ev9xl').click()
    browser.find_element_by_class_name('_ev9xl').send_keys(user)
    browser.find_elements_by_class_name('_ev9xl')[1].click()
    browser.find_elements_by_class_name('_ev9xl')[1].send_keys(password)
    browser.find_element_by_tag_name('button').click()
    return browser


def scrape_profile_info(browser, user_name):
    '''
    INPUT: browser - browser to user, logged into instagram
           user_name - profile to scrape info for
    OUTPUT: info - dictionary of scraped information       
    '''
    # go to profile and click on followers
    browser.get("https://www.instagram.com/{}/".format(user_name))
    time.sleep(2)
    browser.find_element_by_class_name('_h9luf').find_elements_by_tag_name('li')[1].click()
    num_followers = re.sub('followers','', browser.find_elements_by_class_name('_t98z6')[1].text)
    num_followers = int(re.sub(',','', num_followers))
    num_more = num_followers - 20
    # scroll through page
    followers = []
    while len(followers) < num_followers:
        browser.execute_script("""flist= document.getElementsByClassName('_gs38e')[0];
    flist.scrollTop = flist.scrollTopMax; """)
        time.sleep(np.random.normal(2.5, .2))
        follower_tags = browser.find_elements_by_class_name("_2nunc")
        for i in range(len(followers),len(follower_tags)):
            followers.append(follower_tags[i].find_element_by_tag_name('a').text)
        time.sleep(np.random.normal(2.5, .2))
        num_more -=10
        if num_more < -20:
            break
    num_posts = int(re.sub('posts', '', browser.find_elements_by_class_name('_t98z6')[0].text))    
    num_following = int(re.sub('following', '', browser.find_elements_by_class_name('_t98z6')[2].text))
    caption = []
    for elem in browser.find_element_by_class_name("_tb97a").find_elements_by_xpath('*'):
        caption.append(elem.text)
    info = {'num_posts': num_posts, 'caption': caption, 'followers': followers, 'num_following':num_following, 'num_followers': num_followers}
    return info


def make_pickle(to_pickle, pickle_name):
    '''
    INPUT: to_pickle - thing to pickle (like dictionary/dataframe)
           pickle_name - what to call pickle file (ex. thing.pkl)       
    '''
    pickle_out = open(pickle_name,"wb")
    pickle.dump(to_pickle, pickle_out)
    pickle_out.close()