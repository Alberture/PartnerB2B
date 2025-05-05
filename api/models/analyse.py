from django.db import models

from .profile import Profile

ANALYSE_STATUS_CHOICE = [
    ('pending', 'En attente'),
    ('in progress', 'En cours'),
    ('finished', 'Terminé'),
    ('failed', 'Echoué'),
]

class Analyse(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    completedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ANALYSE_STATUS_CHOICE, default='pending')
    score = models.IntegerField(null=True, blank=True)
    details = models.CharField(null=True, blank=True)
    version = models.CharField(null=True, blank=True)
