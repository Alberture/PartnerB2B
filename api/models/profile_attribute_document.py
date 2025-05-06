from django.db import models

from .profile import Profile
from .attribute import Attribute

DOCUMENT_STATUS_CHOICE = [
    ('pending', 'En attente'),
    ('validated', 'Validé'),
    ('rejected', 'Rejeté'),
]

FILE_TYPE = [
    ('pdf', 'PDF'),
    ('jpeg', 'JPEG'),
    ('png', 'PNG'),
    ('txt', 'txt'),
]

TITLE_CHOICE = [
    ('bank_statement', 'Relevé bancaire'),
    ('proof_of_address', 'Justificatif de domicile')
]

class ProfileAttributeDocument(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(choices=TITLE_CHOICE)
    file = models.ImageField(upload_to='documents/')
    type = models.CharField(choices=FILE_TYPE)
    downloadedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DOCUMENT_STATUS_CHOICE, default='pending')
    metadata = models.CharField(null=True, blank=True)
