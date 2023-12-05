from helper_funcs.dateFunctions import get_today

today = get_today().strftime("%Y-%m-%d")
#today = ("2023-11-17")

def parse_response(response):
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

                    insert_statement_to_apppend += f"('{today}','{putCall}', '{contractSymbol}', '{description}', '{bid}', '{ask}', '{low}', '{high}', '{last}', '{mark}', '{volume}', '{openInterest}'), "

    return insert_statement_to_apppend


def get_contracts(response):
    current_symbol_contracts = []
    symbol = response['symbol']

    # either callExpDateMap or putExpDateMap
    for currentMap in response:
        if currentMap != 'callExpDateMap' and currentMap != 'putExpDateMap':
            continue
        for expDate in response[currentMap]:
            for strike in response[currentMap][expDate]:
                for contract in response[currentMap][expDate][strike]:
                    if contract['settlementType'] == 'A':
                        continue
                    if contract['nonStandard']:
                        continue
                    contract['symbol'] = construct_contract_symbol(symbol, expDate, currentMap, strike)
                    current_symbol_contracts.append(contract)
    
    return current_symbol_contracts

def construct_contract_symbol(symbol, exp_date, current_map, strike):
    exp_date = exp_date.split("-")
    exp_year = str(int(exp_date[0]) % 100)
    exp_month = exp_date[1]
    exp_day = exp_date[2].split(":")[0]
    call_put = "C" if current_map == "callExpDateMap" else "P"
    strike = strike if strike.split(".")[1] != '0' else strike.split(".")[0]
    contract_symbol = symbol + exp_year + exp_month + exp_day + call_put + strike
    return contract_symbol

def main():
    from jserver_tools import mock_api_responses
    result = get_contracts(mock_api_responses.mock_td_response)
    print(result)

if __name__ == "__main__":
    main()