from django.db import models

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

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

class AttributeChoice(models.Model):
    """
        Model that represents a choice related to an attriute.
    """
    displayedName = models.CharField(max_length=255)

    def __str__(self):
        return self.displayedName

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
    choices = models.ManyToManyField(AttributeChoice, through='AttributeAttributeChoice')
    regex = models.CharField(null=True, blank=True)
    sensitiveData = models.BooleanField()
    maxLength = models.IntegerField(null=True, blank=True)
    minLength = models.IntegerField(null=True, blank=True)
    maxValue = models.FloatField(null=True, blank=True)
    minValue = models.FloatField(null=True, blank=True)
    isEqualTo = models.FloatField(null=True, blank=True)
    maxDate = models.DateTimeField(null=True, blank=True)
    minDate = models.DateTimeField(null=True, blank=True)
    maxSize = models.IntegerField(null=True, blank=True)
    acceptedFormat = models.CharField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_attribute_or_error(name):
        """
            Method that returns an Attribute with the given id or
            raises an exception if the Attribute was not found
            or pk is invalid.

            param: int pk, id of the Attribute
            return: Attribute
            exceptions: NotFound, ValueError
        """
        try:
            return Attribute.objects.get(name=name)
        except Attribute.DoesNotExist:
            raise NotFound({
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Attribute Not Found",
                "details": [{
                    "field": "name",
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
                        "error": "The attribute name must be a string."
                        }]
                    }
                )

class AttributeAttributeChoice(models.Model):
    """
        Intermediate table to either set an attribute_choice in an attribute choice set
        or tell what attributes is required upon choosing an attribute choice.
    """
    attribute_choice = models.ForeignKey(AttributeChoice, on_delete=models.CASCADE)
    is_choice = models.BooleanField() #If false then choosing this attribute_choice makes the related attribute required
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)