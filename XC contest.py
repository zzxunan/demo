#!/usr/bin/env python
# coding: utf-8

# In[42]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
import csv
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# https://medium.com/p/2d2c25c80c7c
# 
# https://medium.com/towards-data-science/web-scraping-basics-selenium-and-beautiful-soup-applied-to-searching-for-campsite-availability-4a8de1decac9

# In[3]:


import time
from selenium import webdriver

driver = webdriver.Chrome('/path/to/chromedriver') 


# In[8]:


#url = ['https://www.xcontest.org/2021/world/en/flights/daily-score-pg/#filter[date]=2021-01-01@filter[country]=CH@filter[date]=2021-01-01@filter[country]=CH']
driver.get('https://www.xcontest.org/2021/world/en/flights/daily-score-pg/#filter[date]=2021-09-30@filter[country]=US@filter[date]=2021-09-30@filter[country]=US')


# We save the XPath as table_XPath. We can now target the table and extract information from it.
# 
# Each table cell is defined by a <tr> tag for the row and a <td> tag for the column.

# In[9]:


table_XPath = '//*[@id="flights"]/table/tbody/'
num_rows = len(driver.find_elements(by='xpath', value=table_XPath + 'tr')) + 1
num_cols = len(driver.find_elements(by='xpath', value=table_XPath + 'tr[1]/td'))


# In[10]:


table = []
for row in range(1,num_rows):
        row_data = []
        for col in range(1, num_cols):
            text = driver.find_element(by='xpath', value=f'{table_XPath}tr[{row}]/td[{col}]').text
            row_data.append(text)
        table.append(row_data)
    
df = pd.DataFrame(table)
df.head()


# In[23]:


def clean(df):
    # Strip
    df[1] = df.iloc[:,1].str[:5]
    df[['pilot_nationality','pilot']] = df.iloc[:,2].str.split("\n",expand=True)
    df[['country','launch']] = df.iloc[:,3].str.split("\n",expand=True)
    df[5] = df.iloc[:,5].str.rstrip('km')
    df[6] = df.iloc[:,6].str.rstrip('p.')
    # Rename and drop    
    df.rename(columns={1: 'hour', 5: 'distance', 6: 'points', 7: 'km/h'}, inplace=True)
    df.drop([0,2,3,4,8,9,10], axis=1, inplace=True)
    df = df.iloc[:,[0,4,5,6,7,1,2,3]]
    # Clean formats
    df[['distance', 'points', 'km/h']] = df[['distance', 'points', 'km/h']].apply(pd.to_numeric, axis=1)
    df['hour'] = pd.to_datetime(df['hour']).dt.strftime('%H:%M:%S')
    
    return df


# In[28]:


df.head()


# Scrap multiple pages

# In[31]:


def scrap():
    
    table = []
    driver.get(url)
    time.sleep(2)
    table_path = '//*[@id="flights"]/table/tbody/'
    num_rows = len(driver.find_elements(by='xpath', value=table_path + 'tr')) + 1
    num_cols = len(driver.find_elements(by='xpath', value=table_path + 'tr[1]/td'))
    
    for row in range(1,num_rows):
        data = []
        data.append(date)
        for col in range(1, num_cols):
            text = driver.find_element(by='xpath', value=f'{table_path}tr[{row}]/td[{col}]').text
            data.append(text)
        table.append(data)
    
    return pd.DataFrame(table)


# In[74]:


full_df = pd.DataFrame()
date_range = np.arange("2021-09-29","2022-09-30", dtype='datetime64[D]')
#url = f'https://www.xcontest.org/2021/world/en/flights/daily-score-pg/#filter[date]={date}@filter[country]=US@filter[date]={data}@filter[country]=US'
for date in date_range:
    url = f'https://www.xcontest.org/2021/world/en/flights/daily-score-pg/#filter[date]={date}@filter[country]=US@filter[date]={date}@filter[country]=US'
    full_df = full_df.append(scrap())
    time.sleep(2)


# In[75]:


full_df


# In[82]:


temp = full_df.copy()


# In[83]:


temp


# In[84]:


def clean_(df):
    
    # Strip
    df[2] = df.iloc[:,2].str[:5]
    df[['pilot_nationality','pilot']] = df[3].str.split("\n",expand=True)
    df[['country','launch']] = df[4].str.split("\n",expand=True)
    df[6] = df[6].str.rstrip(' km')
    df[7] = df[7].str.rstrip(' p.')
    
    # Rename and drop    
    df.rename(columns={2: 'hour', 6: 'distance', 7: 'points', 8: 'km/h', 0: 'date'}, inplace=True)
    df.drop([1,3,4,5,9,10,11], axis=1, inplace=True)
    #df = df.iloc[:,[4,0,5,6,7,8,1,2,3]]
    
    # Clean formats
    df[['distance', 'points', 'km/h']] = df[['distance', 'points', 'km/h']].apply(pd.to_numeric, axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = pd.to_datetime(df['hour']).dt.strftime('%H:%M:%S')
    
    return df


# In[85]:


new = clean_(temp)


# In[86]:


new


# In[87]:


from pathlib import Path  
filepath = Path('data/out.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
new.to_csv(filepath)  


# In[ ]:




