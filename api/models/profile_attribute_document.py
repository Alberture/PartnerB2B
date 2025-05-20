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
    ('odt', 'ODT'),
]

class ProfileAttributeDocument(models.Model):
    """
        Model that represents a document related to a Profile and Attribute.
        This model is to create dynamic documents for a Profile. 
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='documents/')
    type = models.CharField(choices=FILE_TYPE)
    downloadedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DOCUMENT_STATUS_CHOICE, default='pending')
    metadata = models.CharField(null=True, blank=True)

    def clean(self):
        """
            method that verifies if the validations are correct for a given document
            of a ProfileAttributeDocument.
        """
        if self.attribute.acceptedFormat:
            if not self.type in self.attribute.acceptedFormat.split(";"):
                raise ValidationError({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "This format is not supported for this document",
                        "details": [{
                            "field": "type",
                            "attribute": self.attribute.name, 
                            "error": "accepted file types are : %s" % (self.attribute.acceptedFormat.split(";"))
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
            exceptions: NotFound, ValidationError
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
                "message": "Type Error",
                "details": [{
                        "field": "pk",
                        "pk": pk,
                        "error": "The document id must be an integer"
                        }]
                    }
                )