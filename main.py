from helper_funcs.mysql_functions import insert_into_db, getSymbols
from helper_funcs.api_functions import callAPI
from helper_funcs.contract_table_functions import get_append_contract_data
from helper_funcs.parse_response import parse_response
from tqdm import tqdm

symbol_list = getSymbols()
symbol_list = [
    ('1','AAPL'),
    ('2','BABA'),
    ('3','CMG')
]

untracked_contracts_insert_statement = "INSERT IGNORE INTO Contracts (symbol_id, contract_symbol, description, call_put, strike_price, exp_date) VALUES"

pbar = tqdm(symbol_list, bar_format='{l_bar}{bar:50}{r_bar}{bar:-10b}', colour='green')
for item in pbar:  
    symbol_id = item[0]
    symbol = item[1]
    pbar.set_description("Processing %s" % symbol.center(6))

    response = callAPI(symbol)

    untracked_contracts_insert_statement += get_append_contract_data(response, symbol_id)

untracked_contracts_insert_statement = untracked_contracts_insert_statement[:-1]
insert_into_db(untracked_contracts_insert_statement)