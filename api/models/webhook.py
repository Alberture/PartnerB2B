from django.db import models

from .partner import Partner

import binascii
import os

import requests
from requests.exceptions import MissingSchema, ConnectionError

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status

class Webhook(models.Model):
    """
        Model that reprensents the URL where the API will notify the partner when an analysis
        is done.
    """
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField()
    token = models.CharField(null=True, blank=True)

    def get_webhook_or_error(pk):
        """
            Method that returns a Webhook with the given id or raises an
            exception if the Webhook was not found or pk is invalid.

            param: int pk, id of the Webhook
            return: Webhook
            exceptions: NotFound, ValidationError
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
                    "pk": pk,
                    "error": "The Webhook id must be an integer."
                    }]
                }
            )
        
    def clean(self):
        try:
            requests.post(self.url, json={"key": self.token})
        except ConnectionError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Connection Error",
                "details":[
                    {
                        "field": "url",
                        "error": "We couldn't connect to the given url. Please make sure it is correct."
                    }
                ]
            })
        except MissingSchema:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Missing Schema",
                "details":[
                    {
                        "field": "url",
                        "error": "This is not an url. Perhaps you meant https://%s ?" % (self.url)
                    }
                ]
            })
        
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(20)).decode()
            webhook = Webhook.objects.filter(token=self.token)
            while webhook:
                self.token = binascii.hexlify(os.urandom(20)).decode()
                webhook = Webhook.objects.filter(token=self.token)
        self.clean()
        super().save(*args, **kwargs)
