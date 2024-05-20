from project import GetPriceDatas, RSI, UpdateLog
import pandas as pd
import os
import matplotlib.pyplot as plt
import csv

def test_GetPriceDatas():
    params = {
    "symbol": "BTCUSDT",
    "interval": "5m", 
    "startTime": "",
    "endTime": "",
    "limit": 300
    }

    result = GetPriceDatas(params)
    expectedColumns = ["Date", "Price"]

    # 1 Check that the response type is DataFrame.
    assert isinstance(result, pd.DataFrame)

    # 2 Check that the response is not empty.
    assert not result.empty

    # 3 Check that the response has 2 columns: Date and Price.
    assert all(col in result.columns for col in expectedColumns)

def test_RSI():
    params = {
    "symbol": "BTCUSDT",
    "interval": "5m", 
    "startTime": "",
    "endTime": "",
    "limit": 300
    }

    result = GetPriceDatas(params)
    rsi = RSI(result)

    # Check that the response is not empty.
    assert not rsi.empty

def test_UpdateLog():
    path = "D:\\0_Work\\100_Others\\CS50_P\\FinalProjectSources\\Log\\TradesResult.csv"
    
    dataRow = {
    "Date": "2024-01-17",
    "Time": "17:02",
    "Symbol": "BTCUSDT",
    "Price": "42460,35",
    "Action": "BUY",
    "Total Value": "1000",
    "Realized Profit/Loss": "-",
    "Realized Profit/Loss (%)": "-" 
    }
    
    UpdateLog(path, dataRow)
    # Check that the generated file exist.
    assert os.path.exists(path)

    table = []
    headers = []
    allItems = []

    with open(path) as file:
        reader = csv.reader(file)
        for row in reader:
            allItems.append(row)

        headers = allItems[0]
        for i in allItems[1:]:
            table.append(i)

    # Check if really logged data into the file.
    assert len(table) > 0
  
