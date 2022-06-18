#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[16]:





# In[ ]:





# In[48]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def call_API():
    global dfr
    global pd
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'10',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'c7404f41-23dc-452c-b476-df15a47c3212',
    }

    #c7404f41-23dc-452c-b476-df15a47c3212 personal CoinMarketCAP API Key


    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data_v = json.loads(response.text)
      #print(data_v)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    
    import pandas as pd
    # pd.set_option('display.expand_frame_repr', False)
    # pd.set_option('max_colwidth', -1)
    pd.set_option('display.max_columns', None)
    
    #Pull data into dataframe
#     dfr = pd.json_normalize(data_v['data'])
#     dfr['timestamp'] = pd.to_datetime('now', utc = True)
    
#     dfr2 = pd.json_normalize(data_v['data'])
#     dfr2['timestamp'] = pd.to_datetime('now', utc = True)
    
#     dfr = dfr.append(dfr2)
    
    #Pull data into CSV file
    
    dfr = pd.json_normalize(data_v['data'])
#     dfr['timestamp'] = pd.to_datetime('now', utc = True)
    dfr['timestamp'] = pd.to_datetime('now')
    
    if not os.path.isfile(r'C:\Users\Akinwalesz\Downloads\Personal\PythonAutomationAPIpullrequest\APICryptoData.csv'):
        dfr.to_csv(r'C:\Users\Akinwalesz\Downloads\Personal\PythonAutomationAPIpullrequest\APICryptoData.csv', header = 'column_names')
    else:
        dfr.to_csv(r'C:\Users\Akinwalesz\Downloads\Personal\PythonAutomationAPIpullrequest\APICryptoData.csv', mode = 'a', header =False)
   


# In[49]:


import os
from time import time
from time import sleep

for i in range(300):
    call_API()
    print('API called successfully')
    sleep(90) #pause API call every 90 seconds
exit()


# In[50]:


# pd.set_option('display.max_columns', None)
dfrcsv = pd.read_csv(r'C:\Users\Akinwalesz\Downloads\Personal\PythonAutomationAPIpullrequest\APICryptoData.csv')
dfrcsv


# In[51]:


pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[52]:


dfrcsv1 = dfrcsv.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()
dfcsvstack = dfrcsv1.stack()
# dfrcsv1
dfcsvstack


# In[53]:


# type(dfrcsv1) ---------> pandas.core.frame.DataFrame
# type(dfcsvstack) --------> pandas.core.series.Series

# Convert dfcsvstack to dataframe
dfcsvstack1 = dfcsvstack.to_frame(name= 'Values')
# type(dfcsvstack1) ------> pandas.core.frame.DataFrame
dfcsvstack1


# In[21]:


# dfcsvstack1.count() ---------> 60
# index our stacked dataframe
index = pd.Index(range(60))
dfcsvstack2 = dfcsvstack1.set_index(index)
dfcsvstack2 = dfcsvstack1.reset_index()

dfcsvstack2


# In[54]:


dfcsvstack3 = dfcsvstack2.rename(columns = {'level_1' : '%_Change'})
dfcsvstack3['%_Change'] = dfcsvstack3['%_Change'].replace(['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d'], ['1hr', '24hrs', '7days', '30days', '60days', '90days'])

dfcsvstack3


# In[55]:


import seaborn as sbn
import matplotlib.pyplot as mplt

sbn.catplot(x='%_Change', y='Values', hue='name', data=dfcsvstack3, kind='point')


# In[56]:


dfrsolana = dfrcsv[['name', 'quote.USD.price', 'timestamp']]
dfrsolana = dfrsolana.query("name == 'Solana'")
dfrsolana


# In[57]:


sbn.set_theme(style= 'darkgrid')

sbn.lineplot(x='timestamp', y='quote.USD.price', data=dfrsolana)


# In[ ]:





# In[33]:





# In[ ]:




