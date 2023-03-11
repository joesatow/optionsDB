import mysql.connector
from datetime import datetime, timedelta
from helper_funcs.stockList import getSymbols
import os
import requests

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


for symbol in stockList:
    url = f"https://api.tdameritrade.com/v1/marketdata/chains?apikey={tdAPIkey}&symbol={symbol}&strikeCount=1&fromDate=2022-10-10&toDate={endDate}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    break