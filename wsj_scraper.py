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


# In[2]:


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


# In[3]:


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


# In[4]:


def getArticleContents(covid_articles_urls):
    '''returns article summary text as a list of strings'''
    
    summary_text = ([])
    for i in np.arange(len(covid_articles_urls)):
        # parses url
        headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}
        response = requests.get(covid_articles_urls[i], headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'lxml')
        
        #retrieves and appends summary text
        summary = soup.find('meta', {'name':'article.summary'})['content']
        text = summary.split()
        summary_text = np.append(summary_text, text)
    
    return summary_text

