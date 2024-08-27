from ratelimit import limits, sleep_and_retry, RateLimitException
from datetime import timedelta
from aws_jserver import GetSecret
from .dateFunctions import get_end_date
from .progress_bar import update_tqdm_progress_bar
import datetime
import requests
import pytz
from scripts_jserver import get_access_token

local_tz = pytz.timezone('America/New_York')
#tdAPIkey = GetSecret("TDAmeritrade-API")
strikeCount = 1000
fromDate = datetime.datetime.now(local_tz).strftime("%Y-%m-%d")
endDate = get_end_date(35)
access_token = get_access_token()

period_seconds = 60
@sleep_and_retry
@limits(calls=120, period=timedelta(seconds=period_seconds).total_seconds())
def callAPI(symbol):
    update_tqdm_progress_bar(symbol)

    url = f"https://api.schwabapi.com/marketdata/v1/chains?symbol={symbol}&strikeCount={strikeCount}&fromDate={fromDate}&toDate={endDate}"
    payload={}
    bearer = f"Bearer {access_token}"
    headers = {
        'Authorization': bearer
    }
    
    response = requests.request("GET", url, headers=headers, data=payload).json()

    # if response['status'] == 'FAILED':
    #     print("FAILURE")
    #     print(response)

    if 'error' in response:
        print("error: ")
        print(response)
        raise RateLimitException('custom exception',period_remaining=period_seconds)
    
    key_order = ('symbol', 'callExpDateMap', 'putExpDateMap')
    modified_dict = dict()
    for key in key_order:
        try:
            modified_dict[key] = response[key]
        except:
            print("bad symbol: " + symbol)


    return modified_dict