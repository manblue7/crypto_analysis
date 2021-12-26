import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

pd.options.display.max_columns = None
pd.options.display.max_rows = None



def clean_up(cryptos, drop=False, volume=False, merge=False):
    crypto_now = 'df'
    cryptos_list = []
    if volume == True:
        for crypto in cryptos:
            crypto_now = crypto.drop(columns=['open', 'high', 'low', 'Volume MA', 'close'])
            cryptos_list.append(crypto_now)
        return cryptos_list
    elif drop == True:
        for crypto in cryptos:
            crypto_now = crypto.drop(columns=['open', 'high', 'low', 'Volume', 'Volume MA'])
            cryptos_list.append(crypto_now)
        return cryptos_list
    else:
        for crypto in cryptos:
            crypto_now = pd.read_csv('./crypto_data/{}.csv'.format(crypto))
            cryptos_list.append(crypto_now)
        return cryptos_list
    

# Import current crypto data

cryptos = ['btc', 'eth', 'doge', 'shib', 'ren', 'sol', 'mana', 'ftm', 'atom', 'xlm', 'grt', 'ada'] 
btc, eth, doge, shib, ren, sol, mana, ftm, atom, xlm, grt, ada = clean_up(cryptos)

# Drop data not needed

# Current crypto dataframes
cryptos = [btc, eth, doge, shib, ren, sol, mana, ftm, atom, xlm, grt, ada]

btc_close, eth_close, doge_close, shib_close, ren_close, sol_close, mana_close, ftm_close \
, atom_close, xlm_close, grt_close, ada_close = clean_up(cryptos, drop=True)
print(btc.columns)

btc_vol, eth_vol, doge_vol, shib_vol, ren_vol, sol_vol, mana_vol, ftm_vol \
, atom_vol, xlm_vol, grt_vol, ada_vol = clean_up(cryptos, volume=True)


# Merge all the tables

crypto_close = btc_close.merge(eth_close, on='time', suffixes=('BTC', 'ETH')) \
.merge(shib_close, on='time', suffixes=['ETH','SHIB']) \
.merge(doge_close, on='time', suffixes=['SHIB', 'DOGE']) \
.merge(ren_close, on='time', suffixes=('DOGE', 'REN')) \
.merge(sol_close, on='time', suffixes=('REN', 'SOL')) \
.merge(mana_close, on='time', suffixes=('SOL', 'MANA')) \
.merge(ftm_close, on='time', suffixes=('MANA', 'FTM')) \
.merge(atom_close, on='time', suffixes=('FTM', 'ATOM')) \
.merge(xlm_close, on='time', suffixes=('ATOM', 'XLM')) \
.merge(grt_close, on='time', suffixes=('XLM', 'GRT')) \
.merge(ada_close, on='time', suffixes=('GRT', 'ADA')) 

    
crypto_close.rename(columns={'close' : 'closeREN'}, inplace=True)

crypto_vol = btc_vol.merge(eth_vol, on='time', suffixes=('BTC', 'ETH')) \
.merge(shib_vol, on='time', suffixes=['ETH','SHIB']) \
.merge(doge_vol, on='time', suffixes=['SHIB', 'DOGE']) \
.merge(ren_vol, on='time', suffixes=('DOGE', 'REN')) \
.merge(sol_vol, on='time', suffixes=('REN', 'SOL')) \
.merge(mana_vol, on='time', suffixes=('SOL', 'MANA')) \
.merge(ftm_vol, on='time', suffixes=('MANA', 'FTM')) \
.merge(atom_vol, on='time', suffixes=('FTM', 'ATOM')) \
.merge(xlm_vol, on='time', suffixes=('ATOM', 'XLM')) \
.merge(grt_vol, on='time', suffixes=('XLM', 'GRT')) \
.merge(ada_vol, on='time', suffixes=('GRT', 'ADA'))

print(crypto_close.head())

# change to pct and find the covariance
crypto_close['time'] = pd.to_datetime(crypto_close['time'])
crypto_close.set_index('time', inplace=True)

crypto_vol['time'] = pd.to_datetime(crypto_vol['time'])
crypto_vol.set_index('time', inplace=True)

print('Standard deviation: ')
print(crypto_close.pct_change().std())
print('Correlation: ')
print(crypto_close.pct_change().corr())

#Standard deviation of percent

crypto_close.pct_change().std().plot(kind='bar')
plt.yticks(np.arange(0, .13, 0.01))
plt.show()
plt.close()


#Percent change

crypto_close.pct_change(periods=100).plot()

plt.title('Percent change daily chart of cryptos / te fuck is this shit')
plt.ylabel('%change')
plt.show()

#Covariance heatmap

mask = np.triu(np.ones_like(crypto_close.pct_change(periods=100).cov(), dtype=np.bool))
mask = mask[1:, :-1]
cov= crypto_close.pct_change(periods=100).cov().iloc[1:,:-1].copy()
sns.heatmap(cov, mask=mask, cmap='PuOr', vmin=-1, vmax=1, linewidth=0.3, annot=True)
plt.title('Price Covariance heatmap')
plt.show()
plt.close()

#Correlation heatmap

mask = np.triu(np.ones_like(crypto_close.pct_change().corr(), dtype=np.bool))
mask = mask[1:, :-1]
corr = crypto_close.pct_change().corr().iloc[1:,:-1].copy()
sns.heatmap(corr, mask=mask, cmap='Blues', vmin=0, vmax=1, linewidth=0.3, annot=True)
plt.title('Price Correlation heatmap')
plt.show()
plt.close()

#Volume correlation heatmap
mask = np.triu(np.ones_like(crypto_vol.pct_change().corr(), dtype=np.bool))
mask = mask[1:, :-1]
corr2 = crypto_vol.pct_change().corr().iloc[1:,:-1].copy()
print(crypto_vol.pct_change().corr())
sns.heatmap(corr2, mask=mask, cmap='Blues', vmin=0, vmax=1, linewidth=0.3, annot=True)
plt.title('Volume Correlation')
plt.show()

print(crypto_close.info())




