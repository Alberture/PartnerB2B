from datetime import date

def value_is_between(value, minValue, maxValue, is_date=False):
    """
        Method that says if the given value is between given the minimum value 
        and maximum value. It also works with dates, it must be precised in param.
        The date format for the value is "yyyy-mm-dd".
        
        param: int/float/string value, int/float/date minValue, int/float/date maxValue, boolean is_date
        return: boolean
    """
    if is_date:
        d = date(int(value[:4]), int(value[5:7]), int(value[8:]))
        return d >= minValue and d <= maxValue
    return float(value) >= minValue and float(value) <= maxValue

def value_is_in_attribute_choice_set(attribute, value):
    """
        Method that says is a value is in the attribute choice set.

        param: Attribute attribute, any value
        return: boolean
    """
    exists = attribute.attributechoice_set.order_by("displayedName").filter(displayedName=value)
    if not exists:
        return False
    return True
