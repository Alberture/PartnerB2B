from django.db import models

from .profile import Profile

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

class Document(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    file = models.CharField()
    type = models.CharField(choices=FILE_TYPE)
    downloadedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DOCUMENT_STATUS_CHOICE, default='pending')
    metadata = models.CharField(null=True, blank=True)
