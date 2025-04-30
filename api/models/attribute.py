from django.db import models

TYPE_CHOICE = [
    ('text', 'Texte'),
    ('integer', 'Entier'),
    ('float', 'Décimal'),
    ('date', 'Date'),
    ('boolean', 'Booléen'),
    ('choice', 'Choix'),
    ('json', 'JSON'),
    ('file', 'Fichier'),
]

VALIDATION_CHOICE = [
    ('text', ''),
    ('integer', ''),
    ('float', ''),
    ('date', ''),
    ('boolean', ''),
    ('choice', ''),
    ('json', ''),
    ('file', ''),
]

class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True,)
    displayedName = models.CharField(max_length=255)
    type = models.CharField(choices=TYPE_CHOICE)
    category = models.CharField()
    isRequired = models.BooleanField()
    validation = models.CharField(choices=VALIDATION_CHOICE)
    #Liste choix
    sensitiveData = models.BooleanField()