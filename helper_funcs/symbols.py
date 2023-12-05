from helper_funcs.progress_bar import create_tqdm_progress_bar
from helper_funcs.mysql_functions import get_symbols_from_table

def get_symbols():
    symbols_list = get_symbols_from_table()
    # symbols_list = [
    #     ('1','DHR'),
    #     ('2','BABA'),
    #     ('3','CMG')
    # ]
    return create_tqdm_progress_bar(symbols_list)