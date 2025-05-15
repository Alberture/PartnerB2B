from django.db import models

from .profile import Profile
from .attribute import Attribute

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

DOCUMENT_STATUS_CHOICE = [
    ('pending', 'En attente'),
    ('validated', 'Validé'),
    ('rejected', 'Rejeté'),
]

FILE_TYPE = [
    ('pdf', 'PDF'),
    ('jpeg', 'JPEG'),
    ('png', 'PNG'),
    ('txt', 'TXT'),
    ('ODT', 'TXT'),
]

class ProfileAttributeDocument(models.Model):
    """
        Model that represents a document related to a user and attribute.
        This model is to make attributes dynamic a Documents. 
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ImageField(upload_to='documents/')
    type = models.CharField(choices=FILE_TYPE)
    downloadedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DOCUMENT_STATUS_CHOICE, default='pending')
    metadata = models.CharField(null=True, blank=True)

    def clean(self):
        if not self.type in self.attribute.acceptedFormat:
            raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation Error",
                    "details": [{
                        "field": "type",
                        "attribute": self.attribute.name, 
                        "error": "accepted file types are : %s" % (self.attribute.acceptedFormat)
                    }]
                    }
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_docuement_or_error(pk):
        """
            Method that returns a ProfileAttributeDocument with the given id or 
            raises an exception if the ProfileAttributeDocument was not found
            or pk is invalid.

            param: int pk, id of the ProfileAttributeDocument
            return: ProfileAttributeDocument
            exceptions: NotFound, ValueError
        """
        try:
            return ProfileAttributeDocument.objects.get(pk=pk)
        except ProfileAttributeDocument.DoesNotExist:
            raise NotFound({
                "code": status.HTTP_404_NOT_FOUND,
                "message": "ProfileAttributeDocument Not Found",
                "details": [{
                        "field": "pk",
                        "error": "This document id does not exist. Please try again"
                        }]
                    }
                )

        except ValueError:
            raise ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "TypeError",
                "details": [{
                        "field": "pk",
                        "error": "The document id must be an integer"
                        }]
                    }
                )