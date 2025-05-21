from django.db import models

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

import sys

TYPE_CHOICE = [
    ('string', 'Texte'),
    ('integer', 'Entier'),
    ('float', 'Décimal'),
    ('date', 'Date'),
    ('boolean', 'Booléen'),
    ('choice', 'Choix'),
    ('json', 'JSON'),
    ('file', 'Fichier'),
]

CATEGORIES_CHOICE = [
    ('personal data', 'Données personnelles'),
    ('identity document', 'Pièce d\'identité'),
    ('address', 'Adresse'),
    ('housing situation', 'Situation d\'habitation'),
    ('family situation', 'Situation familiale'),
    ('children', 'Enfants'),
    ('professional situation', 'Situation professionnelle'),
    ('product usage', 'Usage du produit'),
    ('income and expenses', 'Revenus et charge'),
    ('diverse', 'Divers'),
    ('documents', 'Documents'),
]

VALIDATION_CHOICE = [
    ('regex', 'Expression régulière'),
    ('unique choice', 'Choix unique'),
    ('multiple choice', 'Choix multiple'),
    ('min/max value', 'Valeur minmale et maximale'),
    ('min/max length', 'Longueur minmale et maximale'),
    ('min/max date', 'Date minimale et maximale'),
]

class Attribute(models.Model):
    """
        Model that represents a specificity of a Profile or Document.
    """

    name = models.CharField(max_length=255, unique=True)
    displayedName = models.CharField(max_length=255)
    type = models.CharField(choices=TYPE_CHOICE)
    category = models.CharField(choices=CATEGORIES_CHOICE)
    isRequired = models.BooleanField()
    validation = models.CharField(null=True, blank=True, choices=VALIDATION_CHOICE)
    regex = models.CharField(null=True, blank=True)
    sensitiveData = models.BooleanField()
    maxLength = models.IntegerField(null=True, blank=True, default=0)
    minLength = models.IntegerField(null=True, blank=True, default=0)
    maxValue = models.FloatField(null=True, blank=True, default=sys.maxsize)
    minValue = models.FloatField(null=True, blank=True, default=-sys.maxsize - 1)
    maxDate = models.DateField(null=True, blank=True)
    minDate = models.DateField(null=True, blank=True)
    maxSize = models.IntegerField(null=True, blank=True)
    acceptedFormat = models.CharField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_attribute_or_error(name):
        """
            Method that returns an Attribute with the given name or
            raises an exception if the Attribute was not found
            or name is invalid.

            param: string name
            return: Attribute
            exceptions: NotFound, ValidationError
        """
        try:
            return Attribute.objects.get(name=name)
        except Attribute.DoesNotExist:
            raise NotFound({
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Attribute Not Found",
                "details": [{
                    "field": "name",
                    "attribute": name,
                    "error": "This attribute name does not exist. Please try again"
                    }]
                }
            )
        except ValueError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Type Error",
                "details": [{
                        "field": "name",
                        "attribute": name,
                        "error": "The attribute name must be a string."
                        }]
                    }
                )

class AttributeChoice(models.Model):
    """
        Model that represents a choice related to an attriute.
    """
    displayedName = models.CharField()
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.displayedName
    
    def get_attribute_choice_or_error(displayedName):
        """
            Method that returns an AttributeChoice with the given displayedName or
            raises an exception if the Attribute was not found or displayedName 
            is invalid.

            param: string displayedName
            return: AttributeChoice
            exceptions: NotFound, ValueError
        """
        try:
            return AttributeChoice.objects.get(displayedName=displayedName)
        except AttributeChoice.DoesNotExist:
            raise NotFound({
                "code": status.HTTP_404_NOT_FOUND,
                "message": "AttributeChoice Not Found",
                "details": [{
                    "field": "displayedName",
                    "attribute choice": displayedName,
                    "error": "This displayedName name does not exist. Please try again"
                    }]
                }
            )
        except ValueError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Type Error",
                "details": [{
                        "field": "displayedName",
                        "attribute choice": displayedName,
                        "error": "The displayedName name must be a string."
                        }]
                    }
                )
        
    def get_required_attribute_if_chosen(self):
        """
            Method that returns required if this attribute choice
            is chosen.

            return: Attribute or None
        """
        try:
            return self.attributeattributechoice.attribute
        except AttributeChoice.attributeattributechoice.RelatedObjectDoesNotExist:
            return None

class AttributeAttributeChoice(models.Model):
    """
        Intermediate table that link an attribute choice to an attribute.
        The relation can be interpreted as "In this table, if an attribute_choice is related
        to an attribute then if the user choses this attribute_choice, the attribute becomes 
        required".
    """
    attribute_choice = models.OneToOneField(AttributeChoice, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)