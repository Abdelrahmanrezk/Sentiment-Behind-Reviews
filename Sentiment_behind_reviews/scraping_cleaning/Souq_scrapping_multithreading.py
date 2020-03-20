#!/usr/bin/env python
# coding: utf-8

# # Scraping Souq Products
# 
# **Welcome to this scrapping Notebook, what in this notebook:**
# 
# - Implement helpful function that help you scrapp souq products over  thousands of products, along with main features and all reviews of each product.
# - Config file for some intilzation called souq_configs.py.
# - Using firfox geckodriver.
# 
# **Structure of the Scrapping I used:**
# - loading packages we need.
# - path the work dir.
# - connect to cloud mongodb database: some variables defined in souq_configs file.
# - handle some firefox preference and options that help us during process of scrapping
# - at and scraping the products
# - others files like cleaning and features engineering work on these scraped data, actually on  reviews of products
# 

# ### loading packages we need

# In[1]:


from souq_configs import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import pymongo
from time import sleep
import pandas as pd
import numpy as np
import re
import csv
import sys
from time import sleep
from multiprocessing import Process
from selenium.webdriver.common.by import By


# ### Path the work dir

# In[2]:


try:
    current_path = os.path.dirname(os.path.abspath(__file__))
except:
    current_path = '.'


# ### Connect to mongo cloud database
#  - mongo_user: is your used so you need to create account and database after 
#      - link: https://cloud.mongodb.com
#  - mongo_pass: you will get after creating database to connect to this database
#  - mongo_url: database cloud url

# In[3]:


client = pymongo.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_url}")
db = client.SBR


# #### Handle some firefox preference and options that help us during process of scrapping

# In[4]:


def init_driver(gecko_driver='', user_agent='', load_images=True, is_headless=False):
    '''
        This function is just to set up some of default for browser
    '''
    firefox_profile = webdriver.FirefoxProfile()
    
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    firefox_profile.set_preference("media.volume_scale", "0.0")
    firefox_profile.set_preference("dom.webnotifications.enabled", False)
    if user_agent != '':
        firefox_profile.set_preference("general.useragent.override", user_agent)
    if not load_images:
        firefox_profile.set_preference('permissions.default.image', 2)

    options = Options()
    options.add_argument('headless')
#     options.headless = is_headless
    
    driver = webdriver.Firefox(options=options,
                               executable_path=f'{current_path}/{gecko_driver}',
                               firefox_profile=firefox_profile)
    
    return driver


# In[5]:


def get_url(url, driver):
    '''
    Argument:
        url of any page to get
        driver that was inilized
    return:
        True
    '''
    driver.get(url)
    driver.refresh()
    sleep(2)
    return True


# In[6]:


def clean_number(money):
    '''
    Argument:
        a function take a money but as string and clean it,
        to be value that can be used for math operations
        
    return:
        money as float number
    '''

    money = re.findall('[0-9.]', money)
    money = "".join(money)
    return float(money)


# In[7]:


def main_feature(driver2):
    '''
        Argument:
            driver to find elements int the page
        return:
            most of feature related to one product
    '''
# expand to get all information about product
    try:
        show_more = driver2.find_element_by_css_selector(".product-details #specs .expand")
        if len(show_more.text):
            show_more.click()
    except Exception as e:
# send exception to log folder
        file = open("logs_files/main_feature_product.log","+a")
        file.write("This error related to function main_feature of Souq_scrapping_multithreading file\n" 
                   + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines
    '''
        we have got most information about product in above try except
        then for each of these features append to list
        
    '''
    genral_info = []
    genral_info_dd = driver2.find_elements_by_css_selector(".product-details #specs-full dl.stats dd")
    for dd in genral_info_dd:
        if len(dd.text):
            genral_info.append(dd.text)
    return genral_info


# In[8]:


def one_product_reviews(driver2):
    '''
        This functions used to get one product reviews for any product in souq site 
        just pass driver for this product then you will get all reviews
        some of these products have more than 100 reviews but souq display just first 5 reviews
        so we use the button show-more-result to display all reviews then we get all of product reviews
    Argument:
        driver of product page
    return:
        All reviews of this products as list of lists each of them display one use review.
        some of these reviews are arabic and english,
        this handling at second stage of cleaning data we separate them.
    '''
    
    all_reviews_for_one_pro = []
    try:
        show_more = driver2.find_element_by_css_selector("a.show-more-result")
        while True:
# click until the button showmore disappear
            if(len(show_more.text) > 1):
                show_more.click()
# wait one second after each click
                sleep(1)
            else:
                break # break once there no other reviews you can display
                
# after you display all reviews of this product then extract all of them
        reviews = driver2.find_elements_by_css_selector('ul.reviews-list .level-1 p')
    except Exception as e:
        try:
            '''
                some products has a small few reviews so there is no showmore button,
                but maybe has 0 or few reviews so we get also
            '''
            reviews = driver2.find_elements_by_css_selector('ul.reviews-list .level-1 p')
        except:
            pass
# send exception to log folder
        file = open("logs_files/one_product_reviews.log","+a")
        file.write("This error related to function one_product_reviews of Souq_scrapping_multithreading file\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines

    for review in reviews:
        all_reviews_for_one_pro.append(review.text)
        all_pro_reviews.append(review.text)
    return all_reviews_for_one_pro


# ## function explanation
#     
# **This function using the driver of products page to get some of the main attribute of each product:**
# - title
# - url
# - image and others
#     
# **Then the function using another driver to call each product url for other attribute:**
# - main features:
#     - this most of features related to this one product like battery, storage and other
# - reviews:
#     - for each product get all of reviews
# - Database -- each of these product are insearted to our mongo cloud database so:
#     - if product not exist so add new product
#     - if not then check if there are new reviews added
#     - then update some of product info

# In[9]:


def products_info(driver):
    '''
    Argumetn:
        Driver of page with products
    return:
        all info related to these prodcuts for each prodcut
    '''

    products = driver.find_elements_by_css_selector("div.tpl-results div.list-view div.single-item")
    page_products_info = []
    
    for pro in products:
        pro_url        = ''
        pro_title      = ''
        old_price      = ''
        new_price      = ''
        pro_disc_prc   = 0.0
        pro_disc_val   = 0.0
        image_src = ''
        selector = pro.find_elements_by_css_selector
        
# first try to get main info about the product like title and url
        try:
            pro_url = selector('div.item-content a.itemLink')[0].get_attribute('href')
            pro_title = selector('div.item-content a.itemLink h1.itemTitle')[0].text
            new_price = selector('div.col-buy ul.list-blocks li .price-inline .sk-clr1 h3.itemPrice')[0].text
            new_price = clean_number(new_price)
            image_src = selector('a.img-bucket img')
            image_src = image_src[0].get_attribute('data-src')

# check if there is oldprice of this product to get discount
            try:
                len(selector('div.col-buy ul.list-blocks li .price-inline span.itemOldPrice')[0].text)
                old_price = selector('div.col-buy ul.list-blocks li .price-inline span.itemOldPrice')[0].text
                old_price = clean_number(old_price)   
                pro_disc_prc = round(100 - ((new_price / old_price) * 100))
                pro_disc_val = old_price - new_price
            except:
                old_price = 0.0

# Check of this product on our mongo cloud database
            if db.products.count_documents({'$or': [{"product_url": pro_url}, {"product_title":pro_title}]}) == 0:
                
#get the features and reviews of the prodcut
                driver2 = init_driver(gecko_driver,user_agent=user_agent)
                _ = get_url(pro_url, driver2)
                product_reviews = one_product_reviews(driver2)
                main_feature_of_product = main_feature(driver2)
                driver2.close()
                one_product_info = {
                    'product_title'               :pro_title,
                    'product_url'                 : pro_url,
                    'image_src'                   : image_src,
                    'product_new_price'           : new_price,
                    'product_old_price'           : old_price,
                    'product_discount_percentage' : pro_disc_prc,
                    'product_discount_value'      : pro_disc_val,
                    'product_reviews'             : product_reviews,
                    'main_feature_of_product'     : main_feature_of_product,
                    'Uploaded_product'                    : False                   
                }
                _ = db.products.insert_one(one_product_info)
                page_products_info.append(one_product_info)
                
            else:
# once product is exist get it and update it
                pd = db.products.find_one({'$or': [{"product_url": pro_url}, {"product_title":pro_title}]})
                driver2 = init_driver(gecko_driver,user_agent=user_agent)
                _ = get_url(pro_url, driver2)
                reviews_number = driver2.find_element_by_css_selector(".reviewInfo .show_reviews_number")
                reviews_number = int(clean_number(reviews_number.text)) 
                
# no need to call one_product_reviews function and hit the show_more button for just few added reviews
# so comapre different between last count of this product reviews with new added reviews
                if abs(len(pd['product_reviews']) - reviews_number) > 10:
                    product_reviews = one_product_reviews(driver2)
        
                if pd['product_new_price'] != new_price or pd['product_old_price'] != old_price:
                      db.products.update_one({'_id': pd['_id']}, { '$set':{
                        'product_title'               :pro_title,
                        'product_url'                 : pro_url,
                        'product_new_price'           : new_price,
                        'product_old_price'           : old_price,
                        'product_discount_percentage' : pro_disc_prc,
                        'product_discount_value'      : pro_disc_val,
                        'product_reviews'             : product_reviews,
                        }
                                                                
                }) # end of update_one
                    
                driver2.close()
        except Exception as e:
            file = open("logs_files/products_info.log","+a")
            file.write("This error related to function products_info of Souq_scrapping_multithreading file\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines
    return page_products_info
        

      
    


# ## Main Function
# 
# **This function work as follow:**
# - loop over all pages url
# - get driver for each page then after scraping all products quit the page
# - check if there is new page or not to reset the process
# - for each page call product info function which call
#     - main features function
#     - prdocut reviews function
#     - handle money issues and reviews number with clean money
#     - check if the product in the database update it
#     - insert new product if not exist

# In[10]:


def scrap_pages(page_url,next_page = 1):
    '''
    Argument:
        next page = 1 as default value
        page_url to as start page
    return:
        dictionary for all pages contain:
        for each page get all prdocuts info contain:
        for each prodcut get all reviews and main features  
    '''
    all_page_products = {}
    while next_page:
# get the driver first
        url = page_url + str(next_page)
        driver = init_driver(gecko_driver,user_agent=user_agent)
        _ = get_url(url, driver)
# get page products info and for each product get all features and reviews
        products_infos = products_info(driver)
        all_page_products[str(next_page)] = products_info
# check for new pages
        showMore = driver.find_element_by_css_selector('.pagination-next a')
        next_page_url = showMore.get_attribute('href')
        _ = get_url(next_page_url, driver)
        next_page +=1
        current_url = driver.current_url
        driver.close()
# get the page current page number
        current_url = re.findall('page=[0-9]+', current_url)
        current_url = re.findall('[0-9]+', str(current_url))
        current_url = "".join(current_url)
        if current_url != str(next_page):
            next_page = 1
        driver.quit()
    return all_page_products


# In[11]:


if __name__ == '__main__':
    p1 = Process(target=scrap_pages, args=(souq__section_url_apple,1))
    p1.start()
    p2 = Process(target=scrap_pages, args=(souq__section_url_samsung,1))
    p2.start()
    p3 = Process(target=scrap_pages, args=(souq__section_url_huawei,1))
    p3.start()
    p1.join()
    p2.join()
    p3.join()


# # Test 

# '''
# Just convert markdown of this cell to code as test 
# for main_feature and one_product_reviews function
# '''
# driver2 = init_driver(gecko_driver,user_agent=user_agent)
# _ = get_url("https://egypt.souq.com/eg-ar/%D8%A7%D8%A8%D9%84-%D8%A7%D9%8A%D9%81%D9%88%D9%86-7-%D8%A8%D9%84%D8%B3-%D9%85%D8%B9-%D9%81%D9%8A%D8%B3-%D8%AA%D8%A7%D9%8A%D9%85-32-%D8%AC%D9%8A%D8%AC%D8%A7-%D8%A7%D9%84%D8%AC%D9%8A%D9%84-%D8%A7%D9%84%D8%B1%D8%A7%D8%A8%D8%B9-%D8%A7%D9%84-%D8%AA%D9%8A-%D8%A7%D9%8A-%D8%A7%D8%B3%D9%88%D8%AF-11526710/i/", driver2)
# feature = main_feature(driver2)
# reviews = one_product_reviews(driver2)
# print(reviews)
# feature

# ## Test Case shots
# 
# ### snapshot of Main feature function
# ![text](images/features.png "Main feature")
# 
# ### snapshot of error handling for Main feature function
# ![text](images/error_1.png "Error Handling")
# 
# ### snapshot of one_product_reviews function
# ![text](images/reviews.png "Product reviews")
# 
# ### snapshot of error handling for one_product_reviews function
# ![text](images/error_2.png "Error Handling")

# # Go To Cleaning scraped reviews
