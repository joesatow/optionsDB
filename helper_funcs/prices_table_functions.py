from helper_funcs.dateFunctions import get_today

today = get_today().strftime("%Y-%m-%d")

def get_append_prices_data(contract, contract_id):
    insert_statement_to_apppend = "" 
    #INSERT INTO Prices (contract_id, date, bid, ask, low, high, volume, open_interest)

    date = today
    bid = contract['bid']
    ask = contract['ask']
    low = contract['lowPrice']
    high = contract['highPrice']
    volume = contract['totalVolume']
    open_interest = contract['openInterest']
    
    insert_statement_to_apppend += f"('{contract_id}','{date}','{bid}', '{ask}', '{low}', '{high}', '{volume}', '{open_interest}'),"

    return insert_statement_to_apppend

