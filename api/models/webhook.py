from django.db import models

from .partner import Partner

import binascii
import os

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status

class Webhook(models.Model):
    """
        Model that reprensents the URL where the API will notify the partner when an analysis
        is done.
    """
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField()
    key = models.CharField(null=True, blank=True)

    def get_webhook_or_error(pk):
        """
            Method that returns a Webhook with the given id, raises an
            exception if the Webhook was not found or pk is invalid.

            param: int pk, id of the Webhook
            return: Webhook
            exceptions: NotFound, ValueError
        """
        try:
            return Webhook.objects.get(pk=pk)
        except Webhook.DoesNotExist:
            raise NotFound({
                    "code": status.HTTP_404_NOT_FOUND, 
                    "message": "Webhook Not Found", 
                    "details": [{
                        "field": "pk",
                        "error": "This Webhook id does not exist. Please try again."
                    }]
                }
            )
        except ValueError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Type Error", 
                "details": [{
                    "field": "pk",
                    "error": "The Webhook id must be an integer."
                    }]
                }
            )
        
    def save(self, *args, **kwargs):
        if not self.key:
            self.apikeyKey = binascii.hexlify(os.urandom(20)).decode()
            webhook = Webhook.objects.filter(key=self.key)
            while webhook:
                self.key = binascii.hexlify(os.urandom(20)).decode()
                webhook = Webhook.objects.filter(key=self.key)

        super().save(*args, **kwargs)
