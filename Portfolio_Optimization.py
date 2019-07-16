# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:58:01 2019

@author: Darrell
"""
#%% CAPSTONE 1

#%% import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from scipy import mean, std
from scipy.stats import skew, kurtosis
style.use('ggplot')
#%% download data
## from web
start = dt.datetime(2012,1,1)#2000,1,1
end = dt.datetime(2016,12,30)#2000,1,1.today()
aapl = web.DataReader('AAPL','yahoo',start,end)['Adj Close']
cisco = web.DataReader('CSCO','yahoo',start,end)['Adj Close']
ibm = web.DataReader('IBM','yahoo',start,end)['Adj Close']
amzn = web.DataReader('AMZN','yahoo',start,end)['Adj Close']
#%% security risk and return characteristics
stocks=pd.concat([aapl,cisco,ibm,amzn],axis=1)
stocks.columns=['aapl','csco','ibm','amzn']
log_ret=np.log(stocks/stocks.shift(1))# daily log returns
print(log_ret.mean())
print(log_ret.corr())

#%% MCS allocations
np.random.seed(101)
N=5000
all_weights=np.zeros((N,len(stocks.columns)))
ret_arr=np.zeros(N)
vol_arr=np.zeros(N)
sharpe_arr=np.zeros(N)

for i in range(N):
    weights=np.array(np.random.random(len(stocks.columns)))
    weights=weights/np.sum(weights)
    all_weights[i,:]=weights
    # expected portfolio return
    ret_arr[i]=np.sum(log_ret.mean()*weights*252)
    # portfolio return volatility
    vol_arr[i]=np.sqrt(np.dot(weights.T,np.dot(log_ret.cov()*252,weights)))
    sharpe_arr[i]=ret_arr[i]/vol_arr[i]

#%% figure
#fig = plt.figure()
#ax1 = fig.add_subplot(2, 1, 1)
#ax2 = fig.add_subplot(2, 1, 2)
ax1=log_ret.plot(kind='kde') # distribution of daily log returns

#plt.gca().set_xlim(left=-20,right=20)
fig = plt.figure()
ax2=plt.scatter(vol_arr*100,ret_arr*100,c=sharpe_arr)
plt.ylabel('Expected Return (%)')
plt.xlabel('Return Volatility (%)')
plt.colorbar(label='Sharpe Ratio')

# optimum portfolio
opti=sharpe_arr.argmax()
plt.scatter(vol_arr[opti]*100,ret_arr[opti]*100,color='red',marker="x")
#%% optimum asset allocation
print('Optimum allocation =',all_weights[opti,:])