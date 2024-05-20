"""
Return the required data from selected log file.

    Functions:\n
        - GetLog(logPath, mode)\n
        - 
--------------------------------------------------------------------------------------
"""

import csv

table = []
headers = []
allItems = []

modeList = ["table", "heades", "allItems"]
mode = enumerate(modeList)

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

def main():
    ...

def GetLog(logPath: str, mode: enumerate) -> list:
    """
    Get the required data from selected log file.

        Parameters:
            logPath (str): Path of the log file. (E.g.: "D:\\Work\\CS50_P\\FinalProjectSources\\Logs\\Log.csv")
            mode (enumerate):   
                0:table --> all data without the header
                1:header --> only the header of the file
                2:allItems --> all data
                Default: 0:table
        
        Response:
            list (list): Response list based on the selected mode.
    """

    with open(logPath) as file:
        reader = csv.reader(file)
        for row in reader:
            allItems.append(row)

        headers = allItems[0]
        for i in allItems[1:]:
            table.append(i)

    match mode:
        case 0:
            return table
        case 1: 
            return headers
        case 2:
            return allItems
        case _:
            return table

def GetLastLog(logPath: str) -> list:
    """
    Get the last logged data.

        Parameters:
            logPath (str): Path of the log file. (Ex.: "D:\\Work\\CS50_P\\FinalProjectSources\\Logs\\Log.csv")
        
        Response:
            list (list): Last logged data in list format.
    """
    data = GetLog(logPath, 0)
    if len(data) == 0:
        return data
    else:
        return data[-1]

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

if __name__ == "__main__":
    main()