"""
These methods are simple functions to make printing a calendar possible
"""

def day_number(day, month, year):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    year -= month < 3
    return (year + year // 4 - year // 100 + year // 400 + t[month - 1] + day) % 7

def get_month_name(month_number):
    months = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    return months[month_number - 1]

def number_of_days(month_number, year):
    mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if month_number == 2:
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return 29
        else:
            return 28

    else:
        return mdays[month_number]

def get_month_arrays(month_number, year):
    current = day_number(1, month_number, year) - 1

    if current < 0:
        current = 6

    result = [0] * current
    result += list(range(1, number_of_days(month_number, year) + 1))
    if len(result) < 35:
        result += [0] * (35 - len(result))

    return result
