from django.db import models
from . import Attribute

class AttributeChoice(models.Model):
    """
        Model that represents a choice related to an attriute.
    """

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    displayedName = models.CharField(max_length=255)

    def __str__(self):
        return self.displayedName