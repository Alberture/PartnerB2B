from .profile import ProfileBelongsToPartner
from .analysis import AnalysisBelongsToPartner, IsAdminOrHasEnoughTries
from .document import DocumentBelongsToPartnerToRead
from .webhook import ConfigureOnlyIfPartner

__all__ = [
    'ProfileBelongsToPartner',
    "AnalysisBelongsToPartner",
    'DocumentBelongsToPartnerToRead',
    'ConfigureOnlyIfPartner',
    'IsAdminOrHasEnoughTries'
]