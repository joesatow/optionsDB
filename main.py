import mysql.connector
from datetime import datetime, timedelta
from helper_funcs.stockList import getSymbols
import os
import requests
import time

mysqlPass = os.environ['mysqlpass']
tdAPIkey = os.environ['td_api_key']
stockList = getSymbols()

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password=mysqlPass
# )

# print(mydb)

# today = datetime.today().strftime('%Y-%m-%d')
today = datetime.today()
friday = today + timedelta( (4-today.weekday()) % 7 )
endDate = (friday + timedelta(days=35)).strftime('%Y-%m-%d')
endDate = '2023-03-17'


for symbol in stockList:
    url = f"https://api.tdameritrade.com/v1/marketdata/chains?apikey={tdAPIkey}&symbol={symbol}&strikeCount=5&fromDate=2022-10-10&toDate={endDate}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()

    # calls 
    for expDate in response['callExpDateMap']:
        for strike in response['callExpDateMap'][expDate]:
            for contract in response['callExpDateMap'][expDate][strike]:
                print(contract['symbol'])
    
    # puts
    for expDate in response['putExpDateMap']:
        for strike in response['putExpDateMap'][expDate]:
            for contract in response['putExpDateMap'][expDate][strike]:
                print(contract['symbol'])
