from django.db import models

from .profile import Profile
from .attribute import Attribute
from ..utils import value_is_between

from rest_framework import status
from rest_framework.exceptions import ValidationError

import re
from datetime import datetime
import json

class ProfileAttribute(models.Model):
    """
        Model that contains the value of an attribute related to a profile.
        This model is to make attributes dynamic for Profiles.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    source = models.CharField(null=True, blank=True) 

    def clean(self):    
        """
            method that verifies if the validations and type are correct for a given value
            of a ProfileAttribute.
        """
        if self.attribute: 
            match self.attribute.type:       
                case 'integer':
                    try:
                        int(self.value)
                    except ValueError:
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Type Error",
                            "details": [{
                                        "field": "value", 
                                        "attribute": self.attribute.name,
                                        "error": "The value must be an integer."
                                    }]
                                }
                            ) 
                case 'float':
                    try:
                        float(self.value)
                    except ValueError:
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Type Error",
                            "details": [{
                                    "field": "value", 
                                    "attribute": self.attribute.name,
                                    "error": "The value must be a float."
                                    }]
                                }
                            )
                case 'boolean':
                    if not self.value in ('True', 'False'):
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Type Error",
                            "details": [{
                                    "field": "value", 
                                    "attribute": self.attribute.name,
                                    "error": "The value must be a boolean."
                                    }]
                                }
                            )
                case 'date':
                    try:
                        datetime.strptime(self.value, "%Y-%m-%d")
                    except ValueError:
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Type Error",
                            "details": [{
                                        "field": "value", 
                                        "attribute": self.attribute.name,
                                        "error": "The value must be in a correct yyyy-mm-dd format."
                                    }]
                                }
                            )          
                case 'json':
                    try:
                        json.loads(self.value)
                    except json.JSONDecodeError:
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Type Error",
                            "details": [{
                                        "field": "value", 
                                        "attribute": self.attribute.name,
                                        "error": "The value must be JSON."
                                    }]
                                }
                            )
                    
            match self.attribute.validation:
                case 'regex':
                    if not re.match(self.attribute.regex, self.value):
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Regex match invalid",
                            "details": [{
                                "field": "value",
                                "attribute": self.attribute.name, 
                                "error": "the value doesn't match the following regex : %s" % (self.attribute.regex)
                            }]
                            }
                        )
                case 'min/max value':
                    if not value_is_between(self.value, self.attribute.minValue, self.attribute.maxValue):
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Invalid value",
                            "details": [{
                                "field": "value",
                                "attribute": self.attribute.name, 
                                "error": "the value must be between %s and %s." % (self.attribute.minValue, self.attribute.maxValue) 
                            }]
                            }
                        )
                case'min/max length': 
                    if not value_is_between(len(self.value), self.attribute.minLength, self.attribute.maxLength):
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Invalid length",
                            "details": [{
                                "field": "value",
                                "attribute": self.attribute.name, 
                                "error": "the length of the value must be between %s and %s." % (self.attribute.minValue, self.attribute.maxValue) 
                            }]
                            }
                        )  
                case 'min/max date':
                    if not value_is_between(self.value, self.attribute.minDate, self.attribute.maxDate, is_date=True):
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Invalid date",
                            "details": [{
                                "field": "value",
                                "attribute": self.attribute.name, 
                                "error": "the date must be between %s and %s." % (self.attribute.minDate, self.attribute.maxDate) 
                            }]
                            }
                        ) 
    def save(self, **kwargs):
        self.clean()
        return super().save(**kwargs)
    