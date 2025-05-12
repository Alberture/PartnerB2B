from django.db import models

from .partner import Partner

class Webhook(models.Model):
    """
        Model that reprensents the URL where the API will notify the partner when an analysis
        is done.
    """
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField()

