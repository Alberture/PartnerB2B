from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import PermissionDenied

from ..utils import get_authenticated_partner, get_profile_or_error, get_attribute_or_error, valid_response, save_value

from ..serializers import ProfileSerializer, ProfileItemSerializer, ProfileAttributeDocumentSerializer
from ..models import Profile, ProfileAttribute, Attribute
from ..permissions import BelongsToPartnerToGetPatch, IsAdminToDeletePut

class ProfileViewSet(ModelViewSet):
    """
    ViewSet for Profile management (CRUD)
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        IsAuthenticated, 
        BelongsToPartnerToGetPatch,
        IsAdminToDeletePut
    ]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        partner = get_authenticated_partner(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile = serializer.save(partner=partner)
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = get_attribute_or_error(name)
                save_value(value, attribute, profile)

            return valid_response(serializer.data, code=status.HTTP_201_CREATED)

    def retrieve(self, request, pk, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileItemSerializer(profile)
        return valid_response(serializer.data)

    def partial_update(self, request, pk, *args, **kwargs):
        profile = self.get_object()

        serializer = self.get_serializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            profile = serializer.save()
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = get_attribute_or_error(name)
                profile_attribute_qs = ProfileAttribute.objects.filter(profile=profile, attribute=attribute)
                if isinstance(value, list):
                    profile_attribute_qs.delete()
                    for choice in value:
                        save_value(choice, attribute, profile)
                else:
                    save_value(value, attribute, profile, profile_attribute_qs.first())

            return valid_response(serializer.data)
        

    @action(detail=True, methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        profile = self.get_object()
        profile.status = 'complete'
        profile.save()

        return valid_response({
            'status': 'Complet',
            'message': 'Ce profil a été marqué est complet et prêt pour analyse.'
        })

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied(
            {
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Permission Error",
                "details":[{ "error": "You"}]
            }
        )

    def get_object(self):
        profile = get_profile_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, profile)

        return profile
    