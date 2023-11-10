from helper_funcs.stockList import getSymbols
from helper_funcs.mysql_functions import insert_into_db
from helper_funcs.api_functions import callAPI
from helper_funcs.parse_response import parse_response
from tqdm import tqdm

stockList = getSymbols()

insertStatement = "INSERT INTO cons (`date`, `symbol`, `putCall`, `contractSymbol`, `description`, `bid`, `ask`, `low`, `high`, `last`, `mark`, `volume`, `openInterest`) VALUES "

pbar = tqdm(stockList, bar_format='{l_bar}{bar:50}{r_bar}{bar:-10b}', colour='green')
for symbol in pbar:  
    pbar.set_description("Processing %s" % symbol)
    response = callAPI(symbol)

    insertStatement += parse_response(response, symbol)

insertStatement = insertStatement[:-2]
insert_into_db(insertStatement)