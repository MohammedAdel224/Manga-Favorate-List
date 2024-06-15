import re
from datetime import date


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