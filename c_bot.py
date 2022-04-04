from cryptocmd import CmcScraper
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Ploting configurations
FIGSIZE = (12,5)
FONTSIZE_T = 22
FONTSIZE_AX = 14
FONTSIZE_L = 12

# initialise scraper without time interval for max historical data COIN MARKET CAP
scraper = CmcScraper("BTC", "12-12-2017", "04-03-2022")
# Pandas dataFrame for the same data
df = scraper.get_dataframe()
df = df.set_index('Date')
df  =  df.sort_index()

##############################
#MACD, make a raster scan to maximize return
##############################
def MACD(df):
    """

    :param df:
    :return: df with new MACD indicators added
    """
    df['EMA12'] = df.Close.ewm(span=12).mean()
    df['EMA26'] = df.Close.ewm(span=26).mean()
    df['MACD'] = df.EMA12 - df.EMA26
    df['signal'] = df.MACD.ewm(span=9).mean()
    print('MACD Calculations added')

MACD(df)



#BUY AND SELL SIGNALS
buy, sell =[],[]
#loop thorugh df except 2 first rows
for i in range(2, len(df)):
     #         MACD cross signal from bellow triggeres buy signal
    if df.MACD.iloc[i] < df.signal.iloc[i]  and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:
        buy.append(i)

    # MACD cross signal from above triggeres sell signal
    elif df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i - 1] < df.signal.iloc[i - 1]:
        sell.append(i)

buy_array = np.array(buy)
sell_array = np.array(sell)

#plot
fig, ax  = plt.subplots(2,1,figsize= FIGSIZE )
ax[0].plot(df.Close, label = 'BTC Price')
ax[0].scatter(df.iloc[buy_array].index,df.iloc[buy_array].Close,color ='g',marker="^", label ='Buy')
ax[0].scatter(df.iloc[sell_array].index,df.iloc[sell_array].Close,color ='r',marker="v", label ='Sell')
ax[0].axes.xaxis.set_ticklabels([])
ax[0].set_ylabel('Price $', fontsize = FONTSIZE_AX )
ax[0].legend(fontsize = FONTSIZE_L)

ax[1].plot(df.signal,color='r', label = 'Signal')
ax[1].plot(df.MACD,color='g', label = 'MACD')
ax[1].set_xlabel('Date', fontsize = FONTSIZE_AX )
ax[1].set_ylabel('MACD', fontsize = FONTSIZE_AX )
ax[1].legend(fontsize = FONTSIZE_L)

plt.suptitle('BTC Daily MACD Indictaors', fontsize = FONTSIZE_AX )
plt.show()

#BACK TEST

#start with a buy signal
if buy_array[0] < buy_array[0]:
    sell_array = sell_array[1:]


def Back_test(df,i_money, buy, sell):
    #df_trans = pd.DataFrame({'BUY':df.iloc[buy_array].Close.values, 'SELL':df.iloc[sell_array].Close.values})

    for i in range(len(buy_array)):               #carefull with indeces
        btc_invs = i_money / df.iloc[buy_array[i]].Close
        i_money = btc_invs * df.iloc[sell_array[i]].Close
    return i_money#, df_trans

#play with 10,000

#i_money, df_trans =  Back_test(df,10000, buy_array, sell_array)
i_money  =  Back_test(df,10000, buy_array, sell_array)
print(i_money)
# print(df_trans)

#test hold startegy

hold = (1000 / df.Close.values[0]) * df.Close.values[-1]
print(hold)