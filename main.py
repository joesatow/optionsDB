import mysql.connector
from datetime import datetime, timedelta
from helper_funcs.stockList import getSymbols
from ratelimiter import RateLimiter
import os
import requests
import time
import json

mysqlPass = os.environ['mysqlpass']
tdAPIkey = os.environ['td_api_key']
stockList = getSymbols()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=mysqlPass,
  database="options"
)

mycursor = mydb.cursor()

today = datetime.today()
friday = today + timedelta( (4-today.weekday()) % 7 )
endDate = (friday + timedelta(days=35)).strftime('%Y-%m-%d')
#endDate = '2023-03-17'
insertStatement = "INSERT INTO cons (`date`, `symbol`, `putCall`, `contractSymbol`, `description`, `bid`, `ask`, `last`, `mark`, `volume`, `openInterest`) VALUES "
strikeCount = 1000
currentCount = 0

def limited(until):
    global currentCount
    duration = int(round(until - time.time()))
    currentCount = 0
    print('Rate limited, sleeping for {:d} seconds'.format(duration))

@RateLimiter(max_calls=115, period=60, callback=limited)
def callAPI(symbol):
    url = f"https://api.tdameritrade.com/v1/marketdata/chains?apikey={tdAPIkey}&symbol={symbol}&strikeCount={strikeCount}&fromDate=2022-10-10&toDate={endDate}"
    payload={}
    headers = {}
    return requests.request("GET", url, headers=headers, data=payload).json()

for symbol in stockList:
    response = callAPI(symbol)
    currentCount += 1

    if response['status'] == 'FAILED':
        print("error: ")
        print(response)
        continue

    # either callExpDateMap or putExpDateMap
    for currentMap in response:
        if currentMap != 'callExpDateMap' and currentMap != 'putExpDateMap':
            continue
        for expDate in response[currentMap]:
            for strike in response[currentMap][expDate]:
                for contract in response[currentMap][expDate][strike]:
                    #print(json.dumps(contract, indent=2))
                    if contract['settlementType'] == 'A':
                        continue
                    putCall = contract['putCall']
                    contractSymbol = contract['symbol']
                    description = contract['description']
                    bid = contract['bid']
                    ask = contract['ask']
                    last = contract['ask']
                    mark = contract['mark']
                    volume = contract['totalVolume']
                    openInterest = contract['openInterest']

                    insertStatement += f"('{today}', '{symbol}', '{putCall}', '{contractSymbol}', '{description}', '{bid}', '{ask}', '{last}', '{mark}', '{volume}', '{openInterest}'), "

    print(symbol + ' done...' + str(currentCount))                

insertStatement = insertStatement[:-2]
try:
    mySql_insert_query = insertStatement
    mycursor.execute(mySql_insert_query)
    mydb.commit()
    print(mycursor.rowcount, "records inserted successfully into cons table")
    mycursor.close()
except mysql.connector.Error as error:
    print("Failed to insert record into cons table {}".format(error))
finally:
    if mydb.is_connected():
        mydb.close()
        print("MySQL connection is closed")