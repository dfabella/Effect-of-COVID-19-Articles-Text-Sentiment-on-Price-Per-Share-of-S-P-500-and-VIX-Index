#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm_notebook as tqdm_nb
import selenium
from selenium import webdriver
import time
from time import sleep


# In[4]:


# ignore
#def login():
    #browser = webdriver.Chrome(executable_path=r'C:\Users\dfabe\Downloads\chromedriver_win32\chromedriver.exe')
    #browser.get('https://sso.accounts.dowjones.com/login?state=g6Fo2SAyUU9oek1FMEJrT1FoVVREbFRKdXhsMndlQVI5N3NWWqN0aWTZIDNnTnVOS1JaN3R0RnRiOUY5MkRzTFVETVZsekY3NEdoo2NpZNkgNWhzc0VBZE15MG1KVElDbkpOdkM5VFhFdzNWYTdqZk8&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=d29793fe-a288-49a3-84c0-5c59a6465040&ui_locales=en-us-x-wsj-83-2&ns=prod%2Faccounts-wsj&savelogin=on#!/signin')
    
    #username = browser.find_element_by_id('username')
    #username.send_keys('d.fabella13@gmail.com')

    #password = browser.find_element_by_id('password')
    #time.sleep(2)
    #password.send_keys('cogs9stallions!')

    #sing_in = browser.find_element_by_xpath('//button[@class="solid-button basic-login-submit"]')
    #sing_in.click()


# In[5]:


def getTodaysArticles(date):
    '''**IMPORTANT>> date format: YYYY/MM/DD** returns np.array of articles that day'''
    
    next_button = ''
    base_url = 'https://www.wsj.com' 
    date_archive_url ='https://www.wsj.com/news/archive/' + date
    article_urls = np.array([])
    
    while next_button is not None:
        
        # parses url
        headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}
        response = requests.get(date_archive_url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'lxml')
        
        # finds post where article url is stored
        section = soup.find('main')
        posts = section.findAll('article')
        
        #retrieves and appends article urls
        for post in tqdm_nb(posts, leave=False):
            article_url = post.find('a')['href']
            article_urls = np.append(article_urls, article_url)
        
        #checks the page number
        next_button = soup.find('div', {'class':"WSJTheme--SimplePaginator__right--2syX0g5l"})

        #paginator
        if next_button is not None:
            uri = next_button.find('a')['href']
            date_archive_url = base_url + uri
            
    return article_urls


# In[8]:


def getCovidArticles(articles_urls):
    '''returns filtered np.array of COVID articles that day'''
    
    keywords = ['covid', 'coronavirus', 'quarantine', 'test', 'pandemic', 'outbreak', 'in-person', 'reopen', 'closure', 'testing', 'mask', 'ventilator', 'cdc', 'remote', 'fauci', 'virus', 'nurse', 'hospital', 'antibody', 'hot-spot', 'lockdown'] 
    covid_article_urls = ([]) 
    
    for i in np.arange(len(articles_urls)):
    
        for keyword in keywords:
            if (keyword in articles_urls[i]):
                covid_article_urls = np.append(covid_article_urls, articles_urls[i])
                covid_article_urls = np.array(list(set(covid_article_urls)))
    
    return covid_article_urls


# In[11]:


#def getArticleContents(covid_articles_urls):
    
    #content = ([])
    #for i in np.arange(len(covid_articles_urls)):
        #browser = webdriver.Chrome(executable_path=r'C:\Users\dfabe\Downloads\chromedriver_win32\chromedriver.exe')    

        #browser.get(covid_articles_urls[i])
        #browser.implicitly_wait(2)
        #redirect_link = browser.find_element_by_xpath('//a[@class="snippet-btn snippet-sign-in-btn"][@href]')
        #redirect_link.click()

        #username = browser.find_element_by_id('username')
        #username.send_keys('d.fabella13@gmail.com')

        #password = browser.find_element_by_id('password')
        #time.sleep(2)
        #password.send_keys('cogs9stallions!')

        #sing_in = browser.find_element_by_xpath('//button[@class="solid-button basic-login-submit"]')
        #sing_in.click()

        #browser.implicitly_wait(10) # seconds
        #section = browser.find_element_by_class_name("article-content")
        #content = np.append(content, section.text.split())
    
    #return content


# In[12]:


def getArticleContents(covid_articles_urls):
     '''returns text of articles as a list of strings'''
        
    article_text = ([])    
    
    for i in np.arange(len(covid_articles_urls)):
        headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}
        response = requests.get(covid_articles_urls[i], headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'lxml')
        section = soup.find('div', {'class':'wsj-snippet-body'})
        print(covid_articles_urls[i])
    
        if section is not None:
            content = section.text.split()
            article_text = np.append(article_text, content)
            print('article', i+1, 'out of', len(covid_articles_urls))
        
        if section is None:
            print('article', i, 'skipped')
            i +=1
    
    return article_text

