from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework import status

def value_is_between(value, minValue, maxValue, is_date=False):
    """
        Method that says if the given value is between given the minimum value 
        and maximum value. It also works with dates, it must be precised in params.
        The date format for the value is "yyyy-mm-dd".
        
        params: int/float/string value, int/float/date minValue, int/float/date maxValue, boolean is_date
        return: boolean
    """
    if is_date:
        d = date(int(value[:4]), int(value[5:7]), int(value[8:]))
        return d >= minValue and d <= maxValue
    return float(value) >= minValue and float(value) <= maxValue

    