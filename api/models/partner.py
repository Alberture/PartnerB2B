from django.db import models
import binascii
import os

from rest_framework.authtoken.models import Token

STATUS_CHOICE = [
    ('pending', 'en attente'),
    ('in progress', 'en cours'),
    ('success', 'terminé'),
    ('failed', 'échoué')
]

class Partner(models.Model):
    name = models.CharField()
    apiKey = models.CharField(max_length=512, null=True, blank=True)
    activationStatus = models.CharField(choices=STATUS_CHOICE, default='pending')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    webhookUrl = models.CharField(max_length=1000, null=True, blank=True)
    limitUsage = models.PositiveIntegerField()


    def save(self, *args, **kwargs):
        self.apiKey = binascii.hexlify(os.urandom(20)).decode()
        super().save(*args, **kwargs)