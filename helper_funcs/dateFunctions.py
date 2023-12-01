from datetime import datetime, timedelta

today = datetime.today()

def get_today():
    return today

def get_end_date(days_from_now):
    friday = today + timedelta( (4-today.weekday()) % 7 )
    endDate = (friday + timedelta(days=days_from_now)).strftime('%Y-%m-%d')
    return endDate