from .profile import ProfileBelongsToPartner, IsAdminToDeletePut
from .common import IsAdminToDeletePutPatch
from .analysis import AnalysisBelongsToPartnerToRead, IsAdminOrHasEnoughTries
from .document import DocumentBelongsToPartnerToRead
from .webhook import ConfigureOnlyIfPartner

__all__ = [
    'ProfileBelongsToPartner',
    'IsAdminToDeletePut',
    'IsAdminToDeletePutPatch',
    "AnalysisBelongsToPartnerToRead",
    'DocumentBelongsToPartnerToRead',
    'ConfigureOnlyIfPartner',
    'IsAdminOrHasEnoughTries'
]