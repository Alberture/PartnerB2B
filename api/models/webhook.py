from django.db import models

from .partner import Partner

class Webhook(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField()

