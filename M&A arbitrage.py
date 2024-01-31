import DateTime.DateTime
import numpy as np
import pandas as pd
from pandas_datareader import data as web
import yfinance as yfin
from dateutil.relativedelta import relativedelta
from datetime import date
today = date.today()
yfin.pdr_override()
today = date.today()
yfin.pdr_override()
# get a recent M&A deal and test data leakage
# I would go with Broadcom acquisition of Vmware (26 May 2022 announced)
tickers = ['AVGO','0LQO.L']
#loading opening prices for 2 stocks
portfolio = pd.DataFrame()
for ticker in tickers:
    portfolio[ticker] = web.get_data_yahoo(ticker,start = '2022-04-01', end = '2022-07-01')['Open']
# changing column names
column_names = ['Broadcom_Stock_Open_P', 'VMware_Stock_Open_P']
portfolio.columns = column_names
#loading closing prices  for 2 stocks
for ticker in tickers:
    portfolio[ticker] = web.get_data_yahoo(ticker,start = '2022-04-01', end = '2022-07-01')['Adj Close']
# changing column names
portfolio.rename(columns={'AVGO':'Broadcom_Stock_Close_P', '0LQO.L':'VMware_Stock_Close_P'}, inplace= True)
#loading volumes for 2 stocks
for ticker in tickers:
    portfolio[ticker] = web.get_data_yahoo(ticker,start = '2022-04-01', end = '2022-07-01')['Volume']
portfolio.rename(columns={'AVGO':'Broadcom_Stock_Vol', '0LQO.L':'VMware_Stock_Vol'}, inplace= True)
# na values
#print(portfolio.isna().sum())
# drop na
portfolio.dropna(subset = ['VMware_Stock_Open_P'], inplace=True)
#print(portfolio.isna().sum())
# no NA values anymore
# creating a new column in a df and populate with bar color
portfolio['Broadcom_Color'] = np.nan
portfolio['VMware_Color'] = np.nan
#print(portfolio.columns)
# rewrite a column to get color for the volume graph
portfolio['Broadcom_Color'] = ['green' if portfolio.iloc[i]['Broadcom_Stock_Close_P'] >= portfolio.iloc[i]['Broadcom_Stock_Open_P'] else 'red' for i in range(0,len(portfolio))]
portfolio['VMware_Color'] = ['green' if portfolio.iloc[i]['VMware_Stock_Close_P'] >= portfolio.iloc[i]['VMware_Stock_Open_P'] else 'red' for i in range(0,len(portfolio))]
# loading a plotting library + set up the graph
import matplotlib.pyplot as plt
portfolio = portfolio.reset_index()
# build a graph for a Broadcom
plt.style.use('default')
# there are gonna be 2 subplots on top of each other
figure, (ax1,ax2) = plt.subplots(nrows=2, ncols=1)
# first - stock closing price history for the buyer
ax1.plot(portfolio['Date'], portfolio['Broadcom_Stock_Close_P'])
ax1.set_title('Broadcom_Stock_Price')
ax1.axes.get_xaxis().set_visible(False)
ax1.axvspan('2022-05-22','2022-05-28', color='black', alpha=0.5)
# second - trading volumes for the buyer
ax2.bar(portfolio['Date'], portfolio['Broadcom_Stock_Vol'], color = portfolio['Broadcom_Color'])
ax2.set_title('Trading Volumes')
ax2.axvspan('2022-05-22','2022-05-28', color='black', alpha=0.5)
plt.xticks(rotation = 45, ha ='right')
plt.subplots_adjust(bottom=0.2)
# save as an image
plt.savefig('/Users/danilavtonoskin/Desktop/Study/3 Semester/Empirical finance/HW/Efficient Market Hypothesis/Hunter_M&A')
# display the first graphs for the buyer
plt.show()
plt.close()
# creating a graph for seller/target
# I have reduced the timeframe due to an extreme SD in volumes and excluded quite days with minimum trades
adjusted_data = portfolio[(portfolio['Date']>= '2022-05-20') & (portfolio['Date'] < '2022-06-21')]
# second piece of graphs for the seller the same logic
plt.style.use('default')
figure, (ax1,ax2) = plt.subplots(2)
# first graph - closing prices history
ax1.plot(adjusted_data['Date'],adjusted_data['VMware_Stock_Close_P'])
ax1.set_title('VMware_Stock_Price')
ax1.axes.get_xaxis().set_visible(False)
ax1.axvspan('2022-05-25','2022-05-27', color='black', alpha=0.5)
# second graph - trading volumes
ax2.bar(adjusted_data['Date'],adjusted_data['VMware_Stock_Vol'], color = adjusted_data['VMware_Color'])
ax2.set_title('Trading Volumes')
ax2.axvspan('2022-05-25','2022-05-27', color='black', alpha=0.5)
plt.xticks(rotation = 45, ha ='right')
plt.subplots_adjust(bottom=0.2)
# save as an image
plt.savefig('/Users/danilavtonoskin/Desktop/Study/3 Semester/Empirical finance/HW/Efficient Market Hypothesis/Target_M&A')
# display the graph for the target
plt.show()
# as a result, we can see that for the buyer there was a spike (23rd of May 2022) in trades prior to the public announcement of M&A (26th of May 2022) and stock prices went up
# for the target there was also an unusual trading volume noticed (23rd of May 2022) followed by even less volumes on the announcement day, market also reacted positively
# Therefore, looks pretty suspicious
