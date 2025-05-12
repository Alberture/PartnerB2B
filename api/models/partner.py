import binascii
import os

from django.db import models

from rest_framework.authtoken.models import Token

STATUS_CHOICE = [
    ('pending', 'en attente'),
    ('in progress', 'en cours'),
    ('success', 'terminé'),
    ('failed', 'échoué')
]

class Partner(models.Model):
    """
        Model that represents a partner that will use the API.
    """
    name = models.CharField(max_length=255)
    apiKey = models.CharField(max_length=512, null=True, blank=True)
    activationStatus = models.CharField(choices=STATUS_CHOICE, default='pending', max_length=11)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    webhookUrl = models.CharField(max_length=1000, null=True, blank=True)
    limitUsage = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.apiKey = binascii.hexlify(os.urandom(20)).decode()
        partner = Partner.objects.filter(apiKey=self.apiKey)
        while partner:
            self.apiKey = binascii.hexlify(os.urandom(20)).decode()
            partner = Partner.objects.filter(apiKey=self.apiKey)
        super().save(*args, **kwargs)