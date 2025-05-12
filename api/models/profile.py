from django.db import models

from .partner import Partner

PROFILE_STATUS_CHOICE = [
    ('draft', 'Brouillon'),
    ('pending', 'En attente'),
    ('complete', 'Complet'),
    ('in analysis', 'En analyse'),
    ('analyzed', 'Analysé'),
]

class Profile(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=PROFILE_STATUS_CHOICE, default='draft')
    externalReference = models.CharField(null=True, blank=True)

