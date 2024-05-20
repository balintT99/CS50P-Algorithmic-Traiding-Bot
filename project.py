import requests
import pandas as pd 
import datetime as dt 
import matplotlib.pyplot as plt
import time
import csv
import websocket
import json
import os

# region Setup parameters
SLEEP_TIME = 3 # in second
LOG_PATH = "D:\\0_Work\\100_Others\\CS50_P\\FinalProjectSources\\Log\\TradesResult.csv"
JSON_PATH = "D:\\0_Work\\100_Others\\CS50_P\\FinalProjectSources\\Config\\lastData.json"
UNDERVALUED = 30
OVERVALUED = 70

totalAmount = 1000 # total amount in $
endTime = int(dt.datetime.now().timestamp()) * 1000   # Current time
startTime = endTime - (3 * 24 * 60 * 60 * 1000)  # 3 days ago 
symbol = "BTCUSDT" # BTC symbol for feching.
symbolStream = "btcusdt" # BTC symbol for streaming.
interval = "1m"

table = []
headers = []
allItems = []

# Prameters for the data fetching.
params = {
    "symbol": symbol,
    "interval": interval, 
    "startTime": startTime,
    "endTime": endTime,
    "limit": 300 # max 1000 data
}

# Log data row
dataRow = {
    "Date": "-",
    "Time": "-",
    "Symbol": "-",
    "Price": "-",
    "Action": "-",
    "Total Value": "-",
    "Realized Profit/Loss": "-",
    "Realized Profit/Loss (%)": "-" 
}
#endregion

def main():
    holdingPosition = False # default: False
    prevPrice = -1
    os.system("cls")
    print("-------------------Application started.--------------------")
    dfDefault = GetPriceDatas(params)
    while True:
#region Fetch live data
        dfWithoutFirst = dfDefault.tail(-1)
        try:
            GetLatestPrice(symbolStream, interval)
        except Exception as error:
            print("Trading ended up.")
            PlotChart(df,rsi)
            break
    
        with open(JSON_PATH, "r") as f:
            lastData = json.load(f)

        dfNewRow = pd.DataFrame({"Date":[lastData["time"]], "Price":[lastData["price"]]})
        df = dfWithoutFirst._append(dfNewRow, ignore_index=True)
        rsi = RSI(df)
        lastRsi = rsi[len(rsi)]
        lastDate, lastTime = (df.iloc[-1]["Date"]).split(", ")
        lastPrice = df.iloc[-1]["Price"]
        dfDefault = df
        
        PlotChart(df, rsi)

        print("\n")
        print(f"{lastDate} {lastTime}")
        print(f"Price: ${lastPrice}")
        print(f"RSI: {lastRsi}")

        # Build dataRow for logging.
        dataRow["Date"] = lastDate
        dataRow["Time"] = lastTime
        dataRow["Price"] = lastPrice
        dataRow["Symbol"] = symbol
        dataRow["Total Value"] = "$" + str(totalAmount)
#endregion

#region Strategy
        if(lastRsi < UNDERVALUED) and holdingPosition == False:
            dataRow["Action"] = "BUY"
            dataRow["Realized Profit/Loss (%)"] = "-"
            dataRow["Realized Profit/Loss"] = "-"
            holdingPosition = True
            UpdateLog(LOG_PATH, dataRow)
            prevPrice = lastPrice
            print("Action: BUY")
            time.sleep(SLEEP_TIME) # in second

        elif(lastRsi > OVERVALUED) and holdingPosition == True:
            profitPercent = ((lastPrice - prevPrice) / prevPrice) * 100 # Realized Profit/Loss in %
            profit = (((profitPercent / 100) + 1) * totalAmount) - totalAmount # Realized Profit/Loss in $

            profitPercent = "{:.2f}".format(profitPercent)
            profit = "{:.2f}".format(profit)
            
            dataRow["Action"] = "SELL"
            dataRow["Realized Profit/Loss (%)"] = profitPercent + "%"
            dataRow["Realized Profit/Loss"] = "$" + profit
            holdingPosition = False
            UpdateLog(LOG_PATH, dataRow)
            prevPrice = lastPrice
            print("Action: SELL")
            time.sleep(SLEEP_TIME) # in second

        else:
            print("WAIT")
            time.sleep(SLEEP_TIME) # in second


#endregion
    
 #region Functions

def GetPriceDatas(inputParameters: dict):

    """
    Get candlestick bars for a symbol.
    
        Parameters:
            inputParameters (dict): Input parameters for the http request.
                symbol (str): Symbol of the required currency pair. (E.g.: "BTCUSDT")
                interval (str): Timeframe. (E.g.: 1d, 5m, 4w)
                startTime (str): Start time of the candle. (E.g.: 30 days ago --> endTime - (30 * 24 * 60 * 60 * 1000))
                endTime (str): End time of the candle. (E.g.: current time --> int(datetime.now().timestamp()) * 1000))
                limit (int): Number of data points (E.g.: 30 days --> 30)

            If startTime and endTime are not sent, the most recent klines are returned.
        
        Response:
            outputParameters (dict): Response from the http request.
                openTime (int): Candle open time.
                openPrice (str): Open price.
                highPrice (str): High price.
                lowPrice (str): Low price.
                closePrice (str): Close price.
                volume (str): Trade volume.
                closeTime (int): Candle close time.
                numberOfTrades (int): Number of trades.
    """

    requiredParameters = {
            "symbol": "",
            "interval": "",
            "startTime": "",
            "endTime": "",
            "limit": "", 
    }

    if not all(key in inputParameters for key in requiredParameters):
        raise ValueError("Invalid input parameters. Missing required keys.")

    baseUrl = "https://api.binance.com/api/v3/klines" # from https://www.binance.com/en/binance-api

    parameters = {
        "symbol": inputParameters["symbol"],
        "interval": inputParameters["interval"],
        #"startTime": inputParameters["startTime"],
        #"endTime": inputParameters["endTime"],
        "limit": inputParameters["limit"]
    }

    try:    
        response = requests.get(baseUrl, params=parameters) # run the http request with the required parameters

    except Exception as error:
        return("Http error: ",error)

    data = response.json() # get parameters from response 2d array
    
    daily_prices = []
    prices = []
    dates = []

    for kline in data:
        timestamp, open_price, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore = kline
        daily_prices.append({
            "timestamp": (int(timestamp) // 1000),  # Convert milliseconds to seconds
            "open_price": float(open_price),
            "high": float(high),
            "low": float(low),
            "close_price": float(close),
            "volume": float(volume)
        })
        timestamp = timestamp + (60*60*1000) # UTC+1
        prices.append(float(close))
        #dates.append(dt.datetime.utcfromtimestamp(int(timestamp) // 1000).strftime('%Y-%m-%d, %H:%M:%S'))
        dates.append(dt.datetime.fromtimestamp(timestamp / 1000 ).strftime('%Y-%m-%d, %H:%M:%S'))

    df = pd.DataFrame(list(zip(dates, prices)),columns =['Date', 'Price'])

    return df

def RSI(df: pd.DataFrame):
    """
    Get RSI values.
    The relative strength index (RSI) is a momentum indicator used in technical analysis.
    RSI measures the speed and magnitude of a security's recent price changes to evaluate overvalued or undervalued conditions in the price of that security.
    The RSI is displayed as an oscillator (a line graph) on a scale of zero to 100.

        Parameters:
            pd (pandas DataFrame): Needed to get a DataFrame previously. 
        
        Response:
            rsi (pandas DataFrame): Latest RSI values in a list.
    """
    try: 
        change = df["Price"].diff()
        change.dropna(inplace=True)

    except Exception as error:
        print("\n")
        print(df)
        print("\n")
        return("Http error: ",error)

    # Create two copies of the Closing price Series
    change_up = change.copy()
    change_down = change.copy()

    # 
    change_up[change_up < 0] = 0
    change_down[change_down > 0] = 0

    # Verify that we did not make any mistakes
    change.equals(change_up + change_down)

    # Calculate the rolling average of average up and average down
    avg_up = change_up.rolling(14).mean()
    avg_down = change_down.rolling(14).mean().abs()

    rsi = 100 * avg_up / (avg_up + avg_down)

    # Take a look at the 20 oldest datapoints
    rsi.head(20)

    return rsi

def PlotChart(df, rsi):
    """
    Plot 2 charts based on the previous informations (use only for debugging/visualization):
        - Price datas
        - RSI values

        Parameters:
            df (pandas DataFrame): Needed to get a DataFrame previously. 
            rsi (pandas DataFrame): Needed to get a RSI previously. 

        Response:
            Plotted picture.
    """

    df = df[:-1]

    # Set the theme of our chart
    plt.style.use('fivethirtyeight')

    # Make our resulting figure much bigger
    plt.rcParams['figure.figsize'] = (10, 5)

    # Create two charts on the same figure.
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)

    # First chart:
    # Plot the closing price on the first chart
    ax1.plot(df['Date'], df['Price'], linewidth=2)
    ax1.set_title('Bitcoin Price', fontsize= 20)
    ax1.tick_params(axis='x', rotation=15)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(10))

    # Second chart
    # Plot the RSI
    ax2.plot(df["Date"], rsi, color='orange', linewidth=1)
    ax2.set_title('Relative Strength Index', fontsize= 20)
    ax2.tick_params(axis='x', rotation=15)
    ax2.xaxis.set_major_locator(plt.MaxNLocator(10))

    # Add two horizontal lines, signalling the buy and sell ranges.
    # Oversold
    ax2.axhline(UNDERVALUED, linestyle='--', linewidth=1.5, color='green')
    # Overbought
    ax2.axhline(OVERVALUED, linestyle='--', linewidth=1.5, color='red')

    plt.show()

def UpdateLog(logPath: str, data: dir):
    """
    Update the existing csv file.

        Parameters:
            logPath (str): Path of the log file. (Ex.: "D:\\Work\\CS50_P\\FinalProjectSources\\Logs\\Log.csv")
            data (dir): Input data for uploading to log file. Ex.:
                dataRow = {
                    "Date": "2023-12-09",
                    "Time": "12:30",
                    "Symbol": "AAPL",
                    "Price": "150.25",
                    "Action": "BUY",
                    "Total Value": "3000.50",
                    "Realized Profit/Loss": "50.75",
                    "Realized Profit/Loss (%)": "2.15" 
                }
        
        Response:
            list (list): Last logged data in list format.
    """
    dataToCsv = [data["Date"],
                 data["Time"],
                 data["Symbol"],
                 data["Price"],
                 data["Action"],
                 data["Total Value"],
                 data["Realized Profit/Loss"],
                 data["Realized Profit/Loss (%)"],
                 ]
    
    with open(logPath, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dataToCsv)

def GetLatestPrice_message(ws, message):
    message = json.loads(message)
    timestamp = message["E"]
    timestamp = timestamp + (60*60*1000) # UTC+1

    time = dt.datetime.utcfromtimestamp(int(timestamp) // 1000).strftime('%Y-%m-%d, %H:%M:%S')
    price = message["k"]["o"]
    isClosed = message["k"]["x"]
    newRow = {"time": time, "price": float(price)}

    if isClosed:
        with open(JSON_PATH, "w") as f:
            json.dump(newRow, f)
        ws.close()

def GetLatestPrice_error(ws, error):
    None

def GetLatestPrice_close(close_msg):
    print(f"Stream fetch done: {close_msg}")

def GetLatestPrice(symbol, interval):
    socket = f"wss://stream.binance.us:9443/ws/{symbol}@kline_{interval}"
    ws = websocket.WebSocketApp(socket, on_message = GetLatestPrice_message, on_error = GetLatestPrice_error, on_close = GetLatestPrice_close)
    ws.run_forever()

#endregion

if __name__ == "__main__":
    main()