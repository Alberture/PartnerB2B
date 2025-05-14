import binascii
import os

from django.db import models

from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, ValidationError

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
        """
            Method that saves a Partner and creates a new APIkey 
            if doesn't exist.
        """
        if not self.apiKey:
            self.apiKey = binascii.hexlify(os.urandom(20)).decode()
            partner = Partner.objects.filter(apiKey=self.apiKey)
            while partner:
                self.apiKey = binascii.hexlify(os.urandom(20)).decode()
                partner = Partner.objects.filter(apiKey=self.apiKey)
        super().save(*args, **kwargs)

    def get_partner_or_error(apiKey):
        """
            Method that returns a Partner with the given id or 
            raises an exception if the Partner was not found
            or pk is invalid.

            param: int pk, id of the Partner
            return: Partner
            exceptions: NotFound, ValueError
        """
        try:
            return Partner.objects.get(apiKey=apiKey)
        except Partner.DoesNotExist:
            raise NotFound({
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Partner not found",
                "details": [{
                        "field": "apiKey",
                        "error": "The API key was not found."
                        }]
                    }
                )
        
        except ValueError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Type Error",
                "details": [
                    {
                    "field": "pk",
                    "error": "The partner id must be an integer."
                    }
                ]
                }
            )
        
    def get_authenticated_partner(request):
        """
            Method that returns the authenticated
            Partner sending the request.

            param: request
            return: Partner
        """
        token_str = request.META.get('HTTP_AUTHORIZATION', '')[7:]
        validated_token = JWTAuthentication().get_validated_token(token_str)
        user = JWTAuthentication().get_user(validated_token)
        return Partner.objects.get(pk=user.id)
