from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework import status

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

def value_is_in_attribute_choice_set_or_error(attribute, value):
    """
        Method that verifies if a value is in the attribute choice set,
        if not raises a ValidationError.

        param: Attribute attribute, any value
        exceptions: ValidationError
    """
    exists = attribute.attributechoice_set.order_by("displayedName").filter(displayedName=value)
    #dd(exists.first().displayedName)
    if not exists:
        raise ValidationError({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Validation Error.",
            "details":[
                {
                    "field": "value",
                    "error": "The choice must among : %s" % (list(map(str, attribute.attributechoice_set.order_by('displayedName')))),
                    "attribute": attribute.name,
                }
            ]
        })
    
def check_unique_multiple_choices_validation(attribute, value):
    if attribute.validation == 'unique choice':
        if isinstance(value, list) and len(value) != 1:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Validation Error.",
                "details":[
                    {
                        "field": "value",
                        "error": "The choice must be unique among : %s" % (list(map(str, attribute.attributechoice_set.order_by('displayedName')))),
                        "attribute": attribute.name,
                    }
                ]
            })
    elif attribute.validation == 'multiple choice':
        if len(value) < 2 or not isinstance(value, list):
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Validation Error.",
                "details":[
                    {
                        "field": "value",
                        "error": "There must be multiple choices be unique among : %s" % (list(map(str, attribute.attributechoice_set.order_by('displayedName')))),
                        "attribute": attribute.name
                    }
                ]
            })
    