 # Alghoritmic Traiding Bot

 ## Video Demo: [Algorithmic Traiding Bot](https://www.youtube.com/watch?v=BOiA40Xfmg0) 

 ## Description:

 ### About:
Algorithmic trading bots are computer programs designed to execute trading strategies automatically based on predefined rules and algorithms. These bots use mathematical models and statistical analysis to identify potential trading opportunities and make buy or sell decisions in financial markets such as stocks, forex, cryptocurrencies, and commodities.

In this case, I have now created a trading bot for bitcoin trading, but the strategy can be used for any other cryptocurrency or stock market.

This is not financial advice, everyone uses it at their own risk!

### Used APIs:
Binance API: https://api.binance.com

More information: https://binance-docs.github.io/apidocs/spot/en/#general-info

[Binance](https://www.binance.com/en) is one of the world's largest and most popular cryptocurrency exchanges. The platform offers a comprehensive range of cryptocurrency-related services, making it a prominent player in the blockchain and digital asset space.

Binance API (Application Programming Interface) allows developers to interact programmatically with the Binance cryptocurrency exchange. It provides a set of rules and tools for building applications that can access various functionalities offered by Binance.

I used binance *Public Endpoints*  in my code. E.g.:

Check server time:
```python
import requests

# Basic endpoint for GET server time.
baseUrl = "https://api.binance.com/api/v3/time"
response = requests.get(baseUrl)
time = response.json()

print(time)
```

Response:
```cmd
{'serverTime': 1705751904727}
```

### Used pips:
```txt
requests
pandas
matplotlib
websocket-client
pygame
pytest
```

### Logic:
#### Step 1: Fetch Data:
Fetching data from the Binance API involves making HTTP requests to specific endpoints to retrieve information such as market data, account details, and trade history.

#### Step 2: Strategy
Trading strategies are systematic plans or approaches that traders use to make decisions about buying or selling financial instruments in the market. The chosen strategy in this case was monitoring the RSI indicator and checking if already holding a position or not.

#### Step 3: Buy/Sell or Wait
Based on the strategy, in this step it was necessary to decide whether to buy/sell the given position or to wait even longer. At the moment, there is no concrete trading, but I simulate this with a logging method, like a demo.

### Process:
#### Initialization:
The first step is to declare the variables and constants in the code. Create the parameter dicts that will serve as input to the functions. The path to the files must be named here.

Part of the declaration:
```python
totalAmount = 1000 # total amount in $
endTime = int(dt.datetime.now().timestamp()) * 1000   # Current time
startTime = endTime - (3 * 24 * 60 * 60 * 1000)  # 3 days ago 
symbol = "BTCUSDT" # BTC symbol for feching.
symbolStream = "btcusdt" # BTC symbol for streaming.
interval = "5m"
```

```python
params = {
    "symbol": symbol,
    "interval": interval, 
    "startTime": startTime,
    "endTime": endTime,
    "limit": 300 # max 1000 data
}
```

#### Fetch live data:
This part begins by getting a large data set in *GetPriceDatas()*, which is a 300-element DataFrame list. Only the date and price columns need to be filtered out of this list, as the other data will not be needed.

DataFrame:
```cmd
                     Date     Price
0    2024-01-22, 19:15:00  40723.52
1    2024-01-22, 19:20:00  40622.55
2    2024-01-22, 19:25:00  40517.44
3    2024-01-22, 19:30:00  40563.01
4    2024-01-22, 19:35:00  40590.00
..                    ...       ...
295  2024-01-23, 19:50:00  39279.99
296  2024-01-23, 19:55:00  39092.54
297  2024-01-23, 20:00:00  39084.70
298  2024-01-23, 20:05:00  39045.13
299  2024-01-23, 20:10:00  39200.00
```

The second step is to use another query function, named *GetLatestPrice()*, that only queries Binance for the last price and then updates the DataFrame every 5 minutes with the new data. If a new data arrives at the end of the list, we always delete the current first data from the beginning of the list, so creating a LIFO. This function can only run for 24 hours due to Binance restrictions.

Using the resulting DataFrame, we calculate the RSI. The [Relative Strength Index (RSI)](https://en.wikipedia.org/wiki/Relative_strength_index) is a popular momentum oscillator used in technical analysis to assess the magnitude of recent price changes and determine whether a particular asset is overbought or oversold.

RSI result:
```cmd
1            NaN
2            NaN
3            NaN
4            NaN
5            NaN
         ...
295    26.870185
296    21.733846
297    23.586670
298    22.201792
299    30.733066
```

#### Strategy:
Based on the last RSI value, the program must then decide what to do next. 

Three options are possible:

- Buy
- Sell
- Wait

Here, the current open position should be taken into account in addition to the value of the RSI. 

If the RSI value is less than 30 and there are no opened positions, then Buy.
If the RSI value is more than 70 and there is an opened position, then Sell.
In all other cases, Wait.

For example, if we hold a position, we cannot buy it again until we have sold it. And the same is true for selling.

E.g.:

1.

RSI = 57,73

holdingPosition = False
```cmd
2024-01-23 20:10:00
Price: $39200.0
RSI: 57.733065610701438
WAIT
```

2.

RSI = 25,45

holdingPosition = False
```cmd
2024-01-22 14:35:00
Price: $34267.87
RSI: 25.453065610701438
BUY
```

3.

RSI = 28,14

holdingPosition = True
```cmd
2024-01-22 15:05:00
Price: $34704.92
RSI: 28.143065610701438
WAIT
```

As I mentioned, no specific trading takes place here, just a demo process.
There is a file called TradesResult.csv where we log the data for every buy and sell, using *UpdateLog()*:
```csv
Date,Time,Symbol,Price,Action,Total Value,Realized Profit/Loss,Realized Profit/Loss (%)
2024-01-23,20:10:00,BTCUSDT,39223.45,BUY,$1000,-,-
2024-01-23,21:35:00,BTCUSDT,41077.81,SELL,$1000,$1854.36,4.72%
2024-01-24,14:40:00,BTCUSDT,32451.36,BUY,$1000,-,-
2024-01-23,21:35:00,BTCUSDT,33657.37,SELL,$1000,$1206.01,3.71%

```

#### Plot chart:
If the 24 hours have passed and the last data request runs into an error, the *PlotChart()* function creates a chart of the mentioned process based on the DataFrame and RSI lists.
