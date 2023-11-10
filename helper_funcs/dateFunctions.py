from datetime import datetime, timedelta

today = datetime.today()

def get_today():
    return today

def get_end_date():
    friday = today + timedelta( (4-today.weekday()) % 7 )
    endDate = (friday + timedelta(days=35)).strftime('%Y-%m-%d')
    return endDate