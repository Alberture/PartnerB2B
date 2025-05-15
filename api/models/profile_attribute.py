from django.db import models

from .profile import Profile
from .attribute import Attribute, AttributeAttributeChoice
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
        if self.attribute: 
            attribute_type = self.attribute.type
            
            if self.attribute.validation == 'regex' and not re.match(self.attribute.regex, self.value):
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation Error",
                    "details": [{
                        "field": "value",
                        "attribute": self.attribute.name, 
                        "error": "the value doesn't match the following regex : %s" % (self.attribute.regex)
                    }]
                    }
                )
            
            elif self.attribute.validation == 'min/max value' and not value_is_between(self.value, self.attribute.minValue, self.attribute.maxValue):
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation Error",
                    "details": [{
                        "field": "value",
                        "attribute": self.attribute.name, 
                        "error": "the value must be between %s and %s." % (self.attribute.minValue, self.attribute.maxValue) 
                    }]
                    }
                )

            elif self.attribute.validation == 'min/max length' and not value_is_between(len(self.value), self.attribute.minLength, self.attribute.maxLength):
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation Error",
                    "details": [{
                        "field": "value",
                        "attribute": self.attribute.name, 
                        "error": "the length of the value must be between %s and %s." % (self.attribute.minValue, self.attribute.maxValue) 
                    }]
                    }
                )  

            elif self.attribute.validation == 'min/max date' and not value_is_between(self.value, self.attribute.minDate, self.attribute.maxDate, is_date=True):
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation Error",
                    "details": [{
                        "field": "value",
                        "attribute": self.attribute.name, 
                        "error": "the date must be between %s and %s." % (self.attribute.minDate, self.attribute.maxDate) 
                    }]
                    }
                )  

            match attribute_type:
                case 'choice':
                    if not self.value_is_in_choice_set():
                        choice_list = self.attribute.attributechoice_set.order_by('displayedName')
                        raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Validation Error",
                            "details": [{
                                "field": "value", 
                                "attribute": self.attribute.name,
                                "error": "The value must be among the following choices : %s" % (list(map(str, choice_list)))
                                }]
                            }
                        )
                    
                
                    if self.attribute.validation == 'unique choice':
                        choice_list = self.attribute.attributechoice_set.order_by('displayedName')
                        if not self.choice_is_unique():
                            raise ValidationError({
                                "code": status.HTTP_400_BAD_REQUEST,
                                "message": "Validation Error",
                                "details": [{
                                        "field": "value", 
                                        "attribute": self.attribute.name,
                                        "error": "The value must unique among the following choices : %s" %  (list(map(str, choice_list)))
                                    }]
                                }
                            )
                    elif self.choice_is_unique():
                        raise ValidationError({
                                "code": status.HTTP_400_BAD_REQUEST,
                                "message": "Validation Error",
                                "details": [{
                                        "field": "value", 
                                        "attribute": self.attribute.name,
                                        "error": "There must be multiple values among the following choices : %s" %  (list(map(str, choice_list)))
                                    }]
                                }
                            )
        
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


    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
    
    def value_is_in_choice_set(self):
        """
            Method that verifies if the value is in the choice set of an 
            attribute that requires choice(s).
        """
        exists = AttributeAttributeChoice.objects.filter(is_choice=False, attribute_choice__displayedName=self.value, attribute=self.attribute)
        dd(exists.displayedName)
        if not exists:
            return False
        return True
    
    def choice_is_unique(self):
        """
            Method that verifies if the chosen value is unique.
        """
        if self.id:
            return True
        
        values = ProfileAttribute.objects.filter(attribute=self.attribute, profile=self.profile)
        if values:
            return False
        return True
    