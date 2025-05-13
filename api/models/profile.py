from django.db import models

from .partner import Partner

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

PROFILE_STATUS_CHOICE = [
    ('draft', 'Brouillon'),
    ('pending', 'En attente'),
    ('complete', 'Complet'),
    ('in analysis', 'En analyse'),
    ('analyzed', 'Analysé'),
]

class Profile(models.Model):
    """
        Model that represents the partner's client that will be analysed.
    """
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=PROFILE_STATUS_CHOICE, default='draft')
    externalReference = models.CharField(null=True, blank=True)

    def get_profile_or_error(pk):
        """
            Method that returns a Profile with the given id, raises an
            exception if the Profile was not found or pk is invalid.

            param: int pk, id of the Profile
            return: Profile
            exceptions: NotFound, ValueError
        """
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound({
                    "code": status.HTTP_404_NOT_FOUND, 
                    "message": "Profile Not Found", 
                    "details": [{
                        "field": "pk",
                        "error": "This profile id does not exist. Please try again."
                    }]
                }
            )
        except ValueError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Type Error", 
                "details": [{
                    "field": "pk",
                    "error": "The profile id must be an integer."
                    }]
                }
            )