# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 20:25:07 2019

@author: Darrell
"""

#%% CAPSTONE 1
#USER DECISIONS
ticker='VOO' # watchlist: CRM, VOO, SPY
hp = 5 # holding period (years)
#%% import libraries
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from scipy import mean, std
from scipy.stats import skew, kurtosis

style.use('ggplot')
#%% download data
## from web
start = dt.datetime(2000,1,1)#2000,1,1
end = dt.datetime.today()
df = web.DataReader(ticker,'yahoo',start,end)
df_benchmark = web.DataReader('SPY','yahoo',df.index[1],end)
#df.to_csv('TSLA.csv')

## from csv
#df = pd.read_csv('VOO.csv', parse_dates = True, index_col = 0)

#%% moving average
df['20ma'] = df['Adj Close'].rolling(window = 20).mean()
df.dropna(inplace = True)

# historical rate of return
#eR = (df['20ma']['2019'][0]/df['20ma']['2012'][0])**(1/7)

#%% rolling return
returns_cum = df['Adj Close'].pct_change(periods=(252*hp), axis=0)
returns_cum.dropna(inplace = True)
returns_1year = (1.0 + returns_cum)**(1/hp) -1
# benchmark
returns_cum_b = df_benchmark['Adj Close'].pct_change(periods=(252*hp), axis=0)
returns_cum_b.dropna(inplace = True)
returns_1year_b = (1.0 + returns_cum_b)**(1/hp) -1

eR = mean(returns_1year)
sR = std(returns_1year)
eRL = eR - 1.96*sR
eRU = eR + 1.96*sR

#%% figures
#df['Adj Close'].plot()
#plt.show
ax1 = plt.subplot2grid((10,1),(0,0),rowspan=5)
ax2 = plt.subplot2grid((10,1),(6,0),rowspan=5,sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['20ma'])
ax1.set_ylabel('Price (USD)')
ax1.set_title(ticker)
if ticker=='VOO':
    cost_basis=272.91
    diff=dt.date.today()-dt.date(2019,7,2)
    ndays=diff.days
    ax1.axhline(y=cost_basis, color='grey', linestyle='-')
    ax1.axvline(x='2019-07-02', color='grey', linestyle='-')
    print('Your current earnings gross of fees =',5*(df['Adj Close'][-1]-cost_basis))
    print('Your current EAR gross of fees =',
          100*((df['Adj Close'][-1]/cost_basis)**(365/ndays)-1),
          '%')


#ax2.bar(df.index, df['Volume'])
ax2.plot(returns_1year*100, color = 'b')
ax2.axhline(y=eR*100, color='r', linestyle='-')
ax2.axhline(y=0, color='k', linestyle='-')
# benchmark
ax2.plot(returns_1year_b*100, color = 'grey')
ax2.set_ylabel('Trailing Return (%)')
ax2.set_xlabel('Date')
#ax2.xlabel('Date')
#ax2.legend(['rolling return','mean level'])
#ax2.ylabel('Effective Annual Return')

#plt.figure(0)
plt.show()

#plt.plot(returns_1year, color = 'b')
#plt.axhline(y=eR, color='r', linestyle='-')
#plt.axhline(y=0, color='k', linestyle='-')
#plt.xlabel('Date')
#plt.legend(['rolling return','mean level'])
#plt.ylabel('Effective Annual Return')
#plt.figure(1)
