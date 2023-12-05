# INSERT INTO Contracts (symbol_id, contract_symbol, description, call_put, strike_price, exp_date)
def get_append_contract_data(response, symbol_id):
    symbol = response['symbol']
    insert_statement_to_apppend = "" 

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
                    description = contract['description']
                    call_put = contract['putCall']
                    strike_price = contract['strikePrice']
                    contract_symbol = construct_contract_symbol(symbol, expDate, currentMap, strike)
                    exp_date = expDate.split(":")[0]
                    
                    insert_statement_to_apppend += f"('{symbol_id}', '{contract_symbol}', '{description}', '{call_put}', '{strike_price}', '{exp_date}'),"

    return insert_statement_to_apppend

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
    import json
    from jserver_tools import mock_api_responses
    mock_response = mock_api_responses.mock_td_response
    mock_response = json.loads(mock_response)
    parsed = get_append_contract_data(mock_response, 10)
    print(parsed)

if __name__ == "__main__":
    main()