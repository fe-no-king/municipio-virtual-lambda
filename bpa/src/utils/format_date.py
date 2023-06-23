from datetime import datetime

def format_date(date, format="%d-%m-%Y"):

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    
    formatted_date = date_obj.strftime(format)
    return formatted_date

def format_date_br(date, format="%d-%m-%Y"):

    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y %H:%M")
    except ValueError:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    
    formatted_date = date_obj.strftime(format)
    return formatted_date

def calculate_age(date_of_birth):

    try:
        formatted_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        formatted_date = datetime.strptime(date_of_birth, "%d-%m-%Y")

    current_date = datetime.now()
    difference = current_date - formatted_date
    age_in_years = difference.days // 365
    return age_in_years

def format_date_month(date):
    
    date = date.lower()

    months = {
        'jan': '01',
        'fev': '02',
        'mar': '03',
        'abr': '04',
        'mai': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'set': '09',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }
    
    month, year = date.split('/')
    month_number = months.get(month.lower())
    if month_number is None:
        raise ValueError(f"Invalid month abbreviation: {month}")
    
    formatted_date = f"{year}{month_number}"
    return formatted_date

def date_month_format(date):
    
    date = date.lower()

    months = {
        'jan': '01',
        'fev': '02',
        'mar': '03',
        'abr': '04',
        'mai': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'set': '09',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }
    
    month, year = date.split('/')
    month_number = months.get(month.lower())
    if month_number is None:
        raise ValueError(f"Invalid month abbreviation: {month}")
    
    formatted_date = month_number
    return formatted_date