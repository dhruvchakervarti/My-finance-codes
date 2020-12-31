#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from pandas_datareader import data as web
from datetime import datetime 
import seaborn as sns
sns.set()


# In[2]:


stockstartdate = '2020 - 01 -01 '
today = datetime.today().strftime('%Y-%m-%d')
today


# In[3]:


df = web.DataReader('AMZN',data_source = 'yahoo', start = stockstartdate, end  = today)
df


# In[4]:


df['Adj Close'].plot(lw=2, figsize = (10,5), title = 'AMZN Stock Price').set(xlabel='Time',ylabel='AMZN Price')


# In[5]:


OBV = []
OBV.append(0)

for i in range(1,len(df['Adj Close'])):
    if df['Adj Close'][i]>df['Adj Close'][i-1]:
        OBV.append(OBV[-1] + df['Volume'][i])
    elif df['Adj Close'][i]< df['Adj Close'][i-1]:
        OBV.append(OBV[-1] - df['Volume'][i])
    else:
        OBV.append(OBV[-1])
        


# In[6]:


df['OBV'] = OBV
df['OBV_EMA'] = df['OBV'].ewm(span=20).mean()
df


# In[7]:


df.loc[:,['OBV','OBV_EMA']].plot(lw=2, figsize = (10,5), title = 'AMZN OBV/OBV EMA Indicator').set(xlabel='Time',ylabel='AMZN Price')


# In[23]:


# Buy when OBV goes above OBV EMA 
# Sell when OBV EMA goes above OBV
def buy_sell(signal, col1, col2):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    
    for i in range(0,len(signal)):
        if signal[col1][i] > signal[col2][i] and flag != 1:
            sigPriceBuy.append(signal['Adj Close'][i])
            sigPriceSell.append(np.nan)
            flag = 1
        elif signal[col1][i] < signal[col2][i] and flag != 0:
            sigPriceSell.append(signal['Adj Close'][i])
            sigPriceBuy.append(np.nan)
            flag = 0
        else:
            sigPriceSell.append(np.nan)
            sigPriceBuy.append(np.nan)
    return(sigPriceSell,sigPriceBuy)


# In[24]:


x = buy_sell(df,'OBV','OBV_EMA')
df['Buy_Signal_Price'] = x[0]
df['Sell_Signal_Price'] = x[1]


# In[25]:


df


# In[26]:


plt.figure(figsize = (10,5))
plt.plot(df.index,df['Adj Close'], label = 'Adj Close',alpha =0.5)
plt.scatter(df.index, df['Buy_Signal_Price'], label = 'Buy Signal', marker = '^',alpha =1,color='green')
plt.scatter(df.index, df['Sell_Signal_Price'], label = 'Sell Signal', marker = 'v',alpha =1, color = 'red')
plt.title('AMZN Buy Sell Signal')
plt.xlabel('Time')
plt.ylabel('AMZN Price')
plt.legend(loc = 'upperleft')
plt.show()


# In[31]:


PNL = df['Sell_Signal_Price'].sum() - df['Buy_Signal_Price'].sum()
PNL


# In[ ]:




