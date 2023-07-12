from datetime import datetime

from datetime import datetime

def format_date(date, format="%d-%m-%Y"):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            date_obj = datetime.strptime(date, "%m-%Y")

    formatted_date = date_obj.strftime(format)
    return formatted_date