import re
from datetime import date, timedelta


def get_number_from_text(text: str) -> float | None:
    pattern = r'[^sS]?\d+(\.\d+)?'
    result = re.search(pattern, text)
    if result:
        if re.match(r'\d+(\.\d+)?', result.group()):
            return float(result.group())
        return float(result.group()[1:])
    else:
        return None
    
arabic_months = {"يناير": 1,
                 "فبراير": 2,
                 "مارس": 3,
                 "أبريل": 4,
                 "مايو": 5,
                 "يونيو": 6,
                 "يوليو": 7,
                 "أغسطس": 8,
                 "سبتمبر": 9,
                 "أكتوبر": 10,
                 "نوفمبر": 11,
                 "ديسمبر": 12}

def date_from_Arabic(Date):
    month, day, year = Date.string.replace(',', '').split()
    return date(int(year), arabic_months[month], int(day))

def period_to_date(period: str):
    quantity, time_unit, ago = period.split()

    if time_unit == "days":
        delta = timedelta(days=int(quantity))
    elif time_unit == "weeks":
        delta = timedelta(weeks=int(quantity))
    elif time_unit == "hours":
        delta = timedelta(hours=int(quantity))
    elif time_unit == "minutes":
        delta = timedelta(minutes=int(quantity))
    elif time_unit == "seconds":
        delta = timedelta(seconds=int(quantity))
    else:
        return date.today()
    return date.today() - delta

def arabic_period_to_date(period: str):
    parts = period.split()

    if(len(parts) == 2):
        if(parts[1] == "ساعة"):
            delta = timedelta(hours=1)
        elif(parts[1] == "ساعتين"):
            delta = timedelta(hours=2)
        elif(parts[1] == "يوم"):
            delta = timedelta(days=1)
        elif(parts[1] == "يومين"):
            delta = timedelta(days=2)
        elif(parts[1] == "أسبوع"):
            delta = timedelta(weeks=1)
        elif(parts[1] == "أسبوعين"):
            delta = timedelta(weeks=2)
        elif(parts[1] == "شهر"):
            delta = timedelta(days=30)
        elif(parts[1] == "شهرين"):
            delta = timedelta(days=60)
        elif(parts[1] == "سنة"):
            delta = timedelta(days=365)
        elif(parts[1] == "سنتين"):
            delta = timedelta(days=730)
    elif(len(parts) == 3):
        if(parts[2] == "ساعات"):
            delta = timedelta(hours=int(parts[1]))
        elif(parts[2] == "أيام"):
            delta = timedelta(days=int(parts[1]))
        elif(parts[2] == "أسابيع"):
            delta = timedelta(weeks=int(parts[1]))
        elif(parts[2] == "شهور"):
            delta = timedelta(days=30*int(parts[1]))
        elif(parts[2] == "سنوات"):
            delta = timedelta(days=365*int(parts[1]))
    else:
        return date.today()
    return date.today() - delta