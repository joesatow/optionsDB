from helper_funcs.dateFunctions import get_today

today = get_today().strftime("%Y-%m-%d")
today = ("2023-11-11")

def parse_response(response, symbol):
    insert_statement_to_apppend = "" 

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
                    low = contract['lowPrice']
                    high = contract['highPrice']
                    last = contract['ask']
                    mark = contract['mark']
                    volume = contract['totalVolume']
                    openInterest = contract['openInterest']

                    insert_statement_to_apppend += f"('{today}', '{symbol}', '{putCall}', '{contractSymbol}', '{description}', '{bid}', '{ask}', '{low}', '{high}', '{last}', '{mark}', '{volume}', '{openInterest}'), "

    return insert_statement_to_apppend
