from django.db import models
from django.core.exceptions import ValidationError

from .profile import Profile
from .attribute import Attribute

import re
from datetime import datetime

class ProfileAttribute(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    source = models.CharField(null=True, blank=True) 

    def clear(self):
        attribute_type = self.attribute.type
        
        if attribute_type == 'choice':
            if not self.value_is_in_choice_set(self.attribute.attributechoice_set.order_by("displayedName"), self.value):
                raise ValidationError("La donnée n'est pas dans la liste des choix.")
            
            if self.attribute.validation == 'unique choice':
                if not self.choice_is_unique():
                    raise ValidationError("Il ne peut y avoir qu'un seul choix pour cet attribute")
    
        elif self.attribute.validation == 'regex' and not re.search(self.attribute.regex, self.value):
            raise ValidationError("Le format de la donnée n'est pas correcte")
            
        elif attribute_type == 'integer':
            try:
                int(self.value)
            except:
                raise ValidationError("Le format de la donnée n'est pas correcte")
            
        elif attribute_type == 'float':
            try:
                float(self.value)
            except:
                raise ValidationError("Le format de la donnée n'est pas correcte")

        elif attribute_type == 'boolean' and not self.value in ('True', 'False'):
            raise ValidationError("Le format de la donnée n'est pas correcte")

        elif attribute_type == 'date':
            try:
                datetime.strptime(self.value, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("Le format de la donnée n'est pas correcte")

            
    def save(self, *args, **kwargs):
        self.clear()
        return super().save(*args, **kwargs)
    
    def value_is_in_choice_set(self, choice_set, value):
        exists = choice_set.filter(displayedName=value.lower())  
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