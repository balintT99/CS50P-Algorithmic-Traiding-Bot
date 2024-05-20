"""
Return the required currency data from the live blockchain by Binance.

    Functions:\n
        - GetLatestPrice(symbol)\n
        - GetCandlestickBars(inputParameters)\n
--------------------------------------------------------------------------------------
"""

import requests
import json


def main():

    ...

def GetLatestPrice(symbol: str) -> float:
    """
    Get the latest price of the required symbol.

        Parameters:
            symbol (str): The required symbol. (E.g.: "BTCUSDT")
            If neither parameter is sent, prices for all symbols will be returned in an array.
        
        Response:
            currentPrice (float): Latest price in $.
    """

    baseUrl = "https://api.binance.com/api/v3/ticker/price" #from https://www.binance.com/en/binance-api
    parameters = {
        "symbol": symbol
    }

    try:    
        response = requests.get(baseUrl, params=parameters) #run the http request with the required parameters

    except Exception as error:
        return("Http error: ",error)
        
    try:
        data = response.json()
        currentPrice = data["price"] #get price from response dict
    except Exception:
        return("Error occured: Price did not found in received data.\nProbably wrong symbol. (Example: \"BTCUSDT\")")

    return float(currentPrice)

def GetCandlestickBars(inputParameters: dict) -> dict:

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

    baseUrl = "https://api.binance.com/api/v3/klines" #from https://www.binance.com/en/binance-api

    parameters = {
        "symbol": inputParameters["symbol"],
        "interval": inputParameters["interval"],
        "startTime": inputParameters["startTime"],
        "endTime": inputParameters["endTime"],
        "limit": inputParameters["limit"]
    }

    try:    
        response = requests.get(baseUrl, params=parameters) #run the http request with the required parameters

    except Exception as error:
        return("Http error: ",error)

    data = response.json() #get parameters from response 2d array
    outputParameters = { 
        "openTime": data[0][0],
        "openPrice": data[0][1],
        "highPrice": data[0][2],
        "lowPrice": data[0][3],
        "closePrice": data[0][4],
        "volume": data[0][5],
        "closeTime": data[0][6],
        "numberOfTrades": data[0][8]
    }

    return outputParameters

if __name__ == "__main__":
    main()