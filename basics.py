import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


def get_symbol(symbol):
    import requests
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


ticker = input("\nStock Ticker : ").upper()

'''
Setup for future plots
'''
style.use('ggplot')

start = dt.datetime(2016, 1, 1)
end = dt.datetime.now()

# Reading Tesla stock using morningstar
'''
Inputs
1 - Stock code
2 - Data source
3 - Start date
4 - End date

Returns - Pandas dataframe object
'''
df = web.DataReader(ticker, 'morningstar', start, end)

# Removing Stock Symbol and formatting the data
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df = df.drop("Symbol", axis=1)

# Just prints the top of the returned dataframe
print("\n", df.head())

# df['High'].plot()
# plt.legend()
# plt.show()

# Creating a Moving Average through Pandas
df['100ma'] = df['Close'].rolling(window=50, min_periods=0).mean()
print(df.head())

#Plotting Rolling average of Open and Volume in subplots

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
company = get_symbol(ticker)
plt.title(str(company) + " (" + str(ticker) + ")")
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Close'], color="blue")
ax1.plot(df.index, df['100ma'], color="green")
ax2.bar(df.index, df['Volume'], color="red")

plt.show()
