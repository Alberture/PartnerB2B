from django.db import models
from rest_framework.exceptions import ValidationError

from .profile import Profile
from .attribute import Attribute
from rest_framework import status

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
                            "details":[
                                {
                                "field": "value", 
                                "error": "the value doesn't match the following regex : %s" % (self.attribute.regex)
                                }
                            ]
                        })
            
            match attribute_type:
                case 'choice':
                    if not self.value_is_in_choice_set():
                        choice_list = self.attribute.attributechoice_set.order_by('displayedName')
                        raise ValidationError({
                                "code": status.HTTP_400_BAD_REQUEST,
                                "message": "Validation Error",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "The value must be among the following choices : %s" % (list(map(str, choice_list)))
                                    }
                                ]
                            }
                        )
                
                    if self.attribute.validation == 'unique choice':
                        choice_list = self.attribute.attributechoice_set.order_by('displayedName')
                        if not self.choice_is_unique():
                            raise ValidationError({
                                    "status": status.HTTP_400_BAD_REQUEST,
                                    "message": "Validation Error",
                                    "details":[
                                        {
                                        "field": "value", 
                                        "error": "The value must unique among the following choices : %s" %  (list(map(str, choice_list)))
                                        }
                                    ]
                                }
                            )
                        
        
                case 'integer':
                    try:
                        int(self.value)
                    except ValueError:
                        raise ValidationError({
                                    "status":status.HTTP_400_BAD_REQUEST,
                                    "message":"Type Error",
                                    "details":[
                                        {
                                        "field": "value", 
                                        "error": "The value must be an integer."
                                        }
                                    ]
                                }
                            )
        
                case 'float':
                    try:
                        float(self.value)
                    except ValueError:
                        raise ValidationError({
                                    "status":status.HTTP_400_BAD_REQUEST,
                                    "message":"Type Error",
                                    "details":[
                                        {
                                        "field": "value", 
                                        "error": "The value must be a float."
                                        }
                                    ]
                                }
                            )
                    
                case 'boolean':
                    if not self.value in ('True', 'False'):
                        raise ValidationError({
                                    "status":status.HTTP_400_BAD_REQUEST,
                                    "message":"Type Error",
                                    "details":[
                                        {
                                        "field": "value", 
                                        "error": "The value must be a boolean."
                                        }
                                    ]
                                }
                            )
                    
                case 'date':
                    try:
                        datetime.strptime(self.value, "%Y-%m-%d")
                    except ValueError:
                        raise ValidationError({
                                    "status":status.HTTP_400_BAD_REQUEST,
                                    "message":"Type Error",
                                    "details":[
                                        {
                                        "field": "value", 
                                        "error": "The value must be in a correct yyyy-mm-dd format."
                                        }
                                    ]
                                }
                            )
            
                    
                case 'json':
                    try:
                        json.loads(self.value)
                    except json.JSONDecodeError:
                        raise ValidationError({
                                    "status":status.HTTP_400_BAD_REQUEST,
                                    "message":"Type Error",
                                    "details":[
                                        {
                                        "field": "value", 
                                        "error": "The value must be JSON."
                                        }
                                    ]
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
        choice_set = self.attribute.attributechoice_set.order_by("displayedName")
        exists = choice_set.filter(displayedName=self.value)
  
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