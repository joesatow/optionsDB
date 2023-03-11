import mysql.connector
from datetime import datetime, timedelta
from helper_funcs.stockList import getSymbols
from tqdm import tqdm
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
  database="options"
)

mycursor = mydb.cursor()

# today = datetime.today().strftime('%Y-%m-%d')
today = datetime.today()
friday = today + timedelta( (4-today.weekday()) % 7 )
endDate = (friday + timedelta(days=35)).strftime('%Y-%m-%d')
endDate = '2023-03-17'
insertStatement = "INSERT INTO `todaysDate` (`putCall`, `symbol`, `description`, `bid`, `ask`, `last`, `mark`, `openInterest`) VALUES "
strikeCount = 1

for symbol in stockList:
    url = f"https://api.tdameritrade.com/v1/marketdata/chains?apikey={tdAPIkey}&symbol={symbol}&strikeCount={strikeCount}&fromDate=2022-10-10&toDate={endDate}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    if response['status'] == 'FAILED':
        print("error: " + response)
        break
    for currentMap in response:
        if currentMap != 'callExpDateMap' and currentMap != 'putExpDateMap':
            continue
        for expDate in response[currentMap]:
            for strike in response[currentMap][expDate]:
                contract = response[currentMap][expDate][strike][0]
                #print(json.dumps(contract, indent=2))
                putCall = contract['putCall']
                contractSymbol = contract['symbol']
                description = contract['description']
                bid = contract['bid']
                ask = contract['ask']
                last = contract['ask']
                mark = contract['mark']
                openInterest = contract['openInterest']

                insertStatement += f"('{putCall}', '{contractSymbol}', '{description}', '{bid}', '{ask}', '{last}', '{mark}', '{openInterest}'), "

    print(symbol + ' done...')                

insertStatement = insertStatement[:-2]
try:
    mySql_insert_query = insertStatement
    mycursor.execute(mySql_insert_query)
    mydb.commit()
    print(mycursor.rowcount, "records inserted successfully into todaysDate table")
    mycursor.close()
except mysql.connector.Error as error:
    print("Failed to insert record into Laptop table {}".format(error))
finally:
    if mydb.is_connected():
        mydb.close()
        print("MySQL connection is closed")