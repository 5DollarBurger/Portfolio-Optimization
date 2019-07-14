# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:54:51 2019

@author: Darrell
"""

#%% CAPSTONE 2
#%% import libraries
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
#%% download data
## from web
start = dt.datetime(2000,1,1)
end = dt.datetime.today()
df = web.DataReader('VOO','yahoo',start,end)
#df.to_csv('TSLA.csv')

## from csv
#df = pd.read_csv('VOO.csv', parse_dates = True, index_col = 0)
#%% resample to monthly data
df2 = df['Adj Close'].resample('1M').mean()

#%% figures
#df['Adj Close'].plot()
#plt.show

df2.plot()
plt.show()