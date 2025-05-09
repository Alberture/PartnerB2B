from .profile import ProfileBelongsToPartnerToGetPatch, IsAdminToDeletePut
from .common import IsAdminToDeletePutPatch
from .analysis import AnalysisBelongsToPartnerToGetPatch
from .document import DocumentBelongsToPartnerToGetPatch
from .webhook import ConfigureOnlyIfPartner

__all__ = [
    'ProfileBelongsToPartnerToGetPatch',
    'IsAdminToDeletePut',
    'IsAdminToDeletePutPatch',
    "AnalysisBelongsToPartnerToGetPatch",
    'DocumentBelongsToPartnerToGetPatch',
    'ConfigureOnlyIfPartner'
]