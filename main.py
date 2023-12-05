from helper_funcs.mysql_functions import insert_into_db, getContracts
from helper_funcs.api_functions import callAPI
from helper_funcs.contract_table_functions import get_append_contract_data
from helper_funcs.prices_table_functions import get_append_prices_data
from helper_funcs.parse_response import parse_response, get_contracts
from helper_funcs.progress_bar import create_tqdm_progress_bar
from helper_funcs.symbols import get_symbols
from tqdm import tqdm

symbol_list = get_symbols()

untracked_contracts_insert_statement = "INSERT IGNORE INTO Contracts (symbol_id, contract_symbol, description, call_put, strike_price, exp_date) VALUES "
contract_list = []
for item in symbol_list:  
    symbol_id = item[0]
    symbol = item[1]

    response = callAPI(symbol)

    contract_list.extend(get_contracts(response))
    untracked_contracts_insert_statement += get_append_contract_data(response, symbol_id)

insert_into_db(untracked_contracts_insert_statement[:-1], 'Contracts')

db_contracts = dict(getContracts())
prices_insert_statement = "INSERT INTO Prices (contract_id, date, bid, ask, low, high, volume, open_interest) VALUES"
for contract in contract_list:
    contract_symbol = contract['symbol']
    contract_id = db_contracts[contract_symbol]
    prices_insert_statement += get_append_prices_data(contract, contract_id)

insert_into_db(prices_insert_statement[:-1], 'Prices')


# sequence of events
# check for new contracts
# insert prices
