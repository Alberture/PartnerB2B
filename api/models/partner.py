from django.db import models

from rest_framework.authtoken.models import Token

from ..utils import generateAPIKey

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
        self.apiKey = generateAPIKey(self)
        partner = Partner.objects.filter(apiKey=self.apiKey)
        while partner:
            self.apiKey = generateAPIKey(self)
            partner = Partner.objects.filter(apiKey=self.apiKey)
        super().save(*args, **kwargs)