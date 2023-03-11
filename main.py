import mysql.connector
from datetime import datetime, timedelta
from helper_funcs.stockList import getSymbols
import os
import requests
import json

mysqlPass = os.environ['mysqlpass']
tdAPIkey = os.environ['td_api_key']
stockList = getSymbols()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=mysqlPass,
  database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM todaysDate")

myresult = mycursor.fetchall()
for x in myresult:
  print(x)


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
                #print(json.dumps(contract, indent=2))
                putCall = contract['putCall']
                symbol = contract['symbol']
                description = contract['description']
                bid = contract['bid']
                ask = contract['ask']
                last = contract['ask']
                mark = contract['mark']
                openInterest = contract['openInterest']

                string = f"INSERT INTO `todaysDate` (`putCall`, `symbol`, `description`, `bid`, `ask`, `last`, `mark`, `openInterest`) VALUES ('{putCall}', '{symbol}', '{description}', '{bid}', '{ask}', '{last}', '{mark}', '{openInterest}')"
                #print(string)
            break
    break

    # puts
    for expDate in response['putExpDateMap']:
        for strike in response['putExpDateMap'][expDate]:
            for contract in response['putExpDateMap'][expDate][strike]:
                print(contract['symbol'])
