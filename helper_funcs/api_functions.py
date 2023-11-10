from ratelimit import limits, sleep_and_retry, RateLimitException
from datetime import timedelta
from aws_jserver import GetSecret
from helper_funcs.dateFunctions import get_end_date
import requests

tdAPIkey = GetSecret("TDAmeritrade-API")
strikeCount = 1000
endDate = get_end_date()

period_seconds = 60
@sleep_and_retry
@limits(calls=120, period=timedelta(seconds=period_seconds).total_seconds())
def callAPI(symbol):
    url = f"https://api.tdameritrade.com/v1/marketdata/chains?apikey={tdAPIkey}&symbol={symbol}&strikeCount={strikeCount}&fromDate=2022-10-10&toDate={endDate}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()

    if 'error' in response:
        print("error: ")
        print(response)
        raise RateLimitException('custom exception',period_remaining=period_seconds)

    return response