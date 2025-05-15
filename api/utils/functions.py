from datetime import datetime, timedelta

def value_is_between(value, minValue, maxValue, is_date=False):
    if is_date:
        date = datetime(value[:4], value[5:7], value[8:])
        minDate = datetime(minValue[:4], minValue[5:7], minValue[8:])
        maxDate = datetime(maxValue[:4], maxValue[5:7], maxValue[8:])
        return date >= minDate and date <= maxDate
    return value >= minValue and value <= maxValue

def value_is_in_attribute_choice_set(attribute, value):
    exists = attribute.choices.order_by("displayedName").filter(attributeattributechoice__isChoice=True, displayedName=value)
    if not exists:
        return False
    return True