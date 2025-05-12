from django.db import models
from django.core.exceptions import ValidationError

from .profile import Profile
from .attribute import Attribute
#from ..utils import get_expception_error_template

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
        attribute_type = self.attribute.type
     
        if self.attribute.validation == 'regex' and not re.match(self.attribute.regex, self.value):
            raise ValidationError("Le format de la donnée n'est pas correcte")
        
        match attribute_type:
            case 'choice':
                if not self.value_is_in_choice_set():
                    choice_list = self.attribute.attributechoice_set.order_by('displayedName')
                    raise ValidationError({
                            "code": status.HTTP_400_BAD_REQUEST,
                            "message": "Donnée non autorisée",
                            "details":[
                                {
                                "field": "value", 
                                "error": "La donnée doit être parmis les choix suivants : %s" % (list(choice_list))
                                }
                            ]
                        }
                    )
            
                if self.attribute.validation == 'unique choice':
                    choice_list = self.attribute.attributechoice_set.order_by('displayedName')
                    if not self.choice_is_unique():
                        raise ValidationError({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": "Nombre de choix non autorisé",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "La donnée ne peut prendre qu'une valeur parmis les choix suivants : %s" % (list(choice_list))
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
                                "message":"Erreur de type",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "La donnée doit être un entier."
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
                                "message":"Erreur de type",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "La donnée doit être un decimal."
                                    }
                                ]
                            }
                        )
                   
            case 'boolean':
                if not self.value in ('True', 'False'):
                    raise ValidationError({
                                "status":status.HTTP_400_BAD_REQUEST,
                                "message":"Erreur de type",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "La donnée doit être un booléen (True, False)."
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
                                "message":"Erreur de type",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "La donnée doit être une date sous la forme yyyy-mm-dd."
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
                                "message":"Erreur de type",
                                "details":[
                                    {
                                    "field": "value", 
                                    "error": "La donnée doit être au format JSON."
                                    }
                                ]
                            }
                        )
           

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
    
    def value_is_in_choice_set(self):
        choice_set = self.attribute.attributechoice_set.order_by("displayedName")
        exists = choice_set.filter(displayedName=self.value)
  
        if not exists:
            return False
        return True
    
    def choice_is_unique(self):
        if self.id:
            return True
        
        values = ProfileAttribute.objects.filter(attribute=self.attribute, profile=self.profile)
        if values:
            return False
        return True