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
]

class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True)
    displayedName = models.CharField(max_length=255)
    type = models.CharField(choices=TYPE_CHOICE)
    category = models.CharField(choices=CATEGORIES_CHOICE)
    isRequired = models.BooleanField()
    validation = models.CharField(null=True, blank=True, choices=CATEGORIES_CHOICE)
    sensitiveData = models.BooleanField()
