from datetime import datetime, timedelta
import pytz

est = pytz.timezone('US/Eastern')
today = datetime.today().astimezone(est)

def get_today():
    return today

def get_end_date(days_from_now):
    friday = today + timedelta( (4-today.weekday()) % 7 )
    endDate = (friday + timedelta(days=days_from_now)).strftime('%Y-%m-%d')
    return endDate

def main():
    print(get_today())

if __name__ == '__main__':
    main()