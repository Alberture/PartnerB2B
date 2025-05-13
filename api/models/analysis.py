from django.db import models

from .profile import Profile

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

ANALYSIS_STATUS_CHOICE = [
    ('pending', 'En attente'),
    ('in progress', 'En cours'),
    ('finished', 'Terminé'),
    ('failed', 'Echoué'),
]

class Analysis(models.Model):
    """
        Model that represents an analysis of a Profile.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    completedAt = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=ANALYSIS_STATUS_CHOICE, default='pending')
    score = models.IntegerField(null=True, blank=True)
    details = models.CharField(null=True, blank=True)
    version = models.CharField(null=True, blank=True)

    def get_analysis_or_error(pk):
        """
            Method that returns an Analysis with the given id or 
            raises an exception if the Analysis was not found
            or pk is invalid.

            param: int pk, id of the Analysis
            return: Analysis
            exceptions: NotFound, ValueError
        """
        try:
            return Analysis.objects.get(pk=pk)
        except Analysis.DoesNotExist:
            raise NotFound({
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "Analysis not found",
                        "details": [{
                            "field": "pk",
                            "error": "This analysis does not exist. Please try again."
                        }]
                    }
                )
        
        except ValueError:
            raise ValidationError({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Type Error",
                        "details": [{
                            "field": "pk",
                            "error": "The analysis id must be an integer."
                        }]
                    }
                )
