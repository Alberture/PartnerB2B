from .profile import ProfileBelongsToPartner
from .analysis import AnalysisBelongsToPartner, IsAdminOrHasEnoughTries
from .document import DocumentBelongsToPartnerToRead
from .webhook import WebhookBelongsToParnter

__all__ = [
    'ProfileBelongsToPartner',
    "AnalysisBelongsToPartner",
    'DocumentBelongsToPartnerToRead',
    'WebhookBelongsToParnter',
    'IsAdminOrHasEnoughTries'
]