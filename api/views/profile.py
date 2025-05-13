from rest_framework.viewsets import ModelViewSet
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import PermissionDenied

from ..utils import valid_response

from ..serializers import ProfileSerializer, ProfileItemSerializer, ProfileAttributeSerializer
from ..models import Profile, ProfileAttribute, Attribute, Partner
from ..permissions import ProfileBelongsToPartner, IsAdminToDeletePut

from drf_spectacular.utils import extend_schema, OpenApiExample


from datetime import datetime

class ProfileViewSet(ModelViewSet):
    """
        ViewSet that manages Profile objects.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        IsAuthenticated, 
        ProfileBelongsToPartner,
        IsAdminToDeletePut
    ]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(
        request=ProfileSerializer,
        examples=[
            OpenApiExample(
            name="Example request body for create Profile",
            value={
                'external_reference': 'reference',
                'attributes': {
                    'firstname': 'Jean',
                    'lastname': 'Dupont',
                    'means_of_movement': [
                        'bike',
                        'motobike',
                        'walking'
                    ]
                }
            },
            request_only=True
            ),
            OpenApiExample(
            name="Exemple create Profile",
            value={
                "data":{
                    "pk": 0,
                    "status": "draft",
                    "createdAt": "2025-05-12T09:06:36.335Z",
                    "profileattribute_set": [
                        {"attribute": {"name": "firstname"}, "value": "Jean"},
                        {"attribute": {"name": "lastname"}, "value": "Dupont"},
                        {"attribute": {"name": "means_of_movement"},"value": "bike"},
                        {"attribute": { "name": "means_of_movement"},"value": "motobike"},
                        {"attribute": {"name": "means_of_movement"},"value": "walking"},
                    ]
                },
                "meta":{
                    "timestamp": datetime.now()
                }
                
            },
            response_only=True
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        partner = Partner.get_authenticated_partner(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile = serializer.save(partner=partner)
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = Attribute.get_attribute_or_error(name)

                if isinstance(value, list):
                    for choice in value:
                        self.save_value(choice, attribute, profile)
                else:
                    self.save_value(value, attribute, profile)

            return valid_response(serializer.data, request.id, code=status.HTTP_201_CREATED)
    

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Exemple retrieve Profile",
            value={
                "data": {
                    "createdAt": "2025-05-09T12:15:03.881476Z",
                    "updatedAt": "2025-05-09T12:15:03.881509Z",
                    "status": "sketch",
                    "externalReference": "",
                    "profileattribute_set": [
                        {"attribute": {"name": "firstname"},"value": "Nom"},
                        {"attribute": {"name": "lastname"},"value": "Prenom"},
                        { "attribute": {"name": "gender"},"value": "M"},
                        { "attribute": { "name": "professional_situation" },"value": "autre"},
                        { "attribute": {"name": "professional_situation"},"value": "salarié"},
                        {"attribute": {"name": "professional_situation"},"value": "étudiant"}
                    ],
                    "last_analyse": {
                        "score": None,
                        "status": "pending",
                        "details": None,
                        "version": None
                    }
                },
                "meta": {
                    "timestamp": "2025-05-12T10:11:43.627984"
                }
            },
            response_only=True
            )
        ]
    )
    def retrieve(self, request, pk, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileItemSerializer(profile)
        return valid_response(serializer.data, request.id)


    @extend_schema(
        request=ProfileSerializer,
        examples=[
            OpenApiExample(
            name="Example body for update Profile",
            value={
                'external_reference': 'reference',
                'attributes': {
                    'firstname': 'Jean',
                    'lastname': 'Dupont',
                    'means_of_movement': [
                        'bike',
                        'motobike',
                        'walking'
                    ]
                }
            },
            request_only=True
            ),
            OpenApiExample(
            name="Example update Profile",
            value={
                "pk": 0,
                "status": "draft",
                "createdAt": "2025-05-12T09:06:36.335Z",
                "profileattribute_set": [
                    {"attribute": {"name": "firstname"}, "value": "Jean"},
                    {"attribute": {"name": "lastname"}, "value": "Dupont"},
                    {"attribute": {"name": "means_of_movement"},"value": "bike"},
                    {"attribute": { "name": "means_of_movement"},"value": "motobike"},
                    {"attribute": {"name": "means_of_movement"},"value": "walking"},
                ]
            },
            response_only=True
            )
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        profile = self.get_object()

        serializer = self.get_serializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            profile = serializer.save()
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = Attribute.get_attribute_or_error(name)
                profile_attribute_qs = ProfileAttribute.objects.filter(profile=profile, attribute=attribute)
                if isinstance(value, list):
                    profile_attribute_qs.delete()
                    for choice in value:
                        self.save_value(choice, attribute, profile)
                else:
                    self.save_value(value, attribute, profile, profile_attribute_qs.first())

            return valid_response(serializer.data, request.id)
        

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Example submit Profile",
            value={
                "data": {
                    "status": "Complet",
                    "message": "Ce profil a été marqué est complet et prêt pour analyse."
                },
                "meta": {
                    "timestamp": "2025-05-12T10:24:45.337404"
                }
            },
            response_only=True
            )
        ]
    )
    @action(detail=True, methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        profile = self.get_object()
        profile.status = 'complete'
        profile.save()

        return valid_response({
            'status': 'Complet',
            'message': 'Ce profil a été marqué est complet et prêt pour analyse.'
        }, request.id)

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        raise PermissionDenied({
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Permission Denied",
            "details": [
                {"error": "You must be an admin to perform this action."}
            ]
        })
    
    @extend_schema(exclude=True)
    def destroy(self, request, pk, *args, **kwargs):
        return super().destroy(request, pk, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def update(self, request, pk, *args, **kwargs):
        return super().update(request, pk, *args, **kwargs)

    def get_object(self):
        profile = Profile.get_profile_or_error(self.kwargs["pk"])
        self.check_object_permissions(self.request, profile)

        return profile
    
    def save_value(self, value, attribute, profile, instance=None):
        """
            Method that creates a ProfileAttribute with the given Attribute,
            Profile and value or edits an instance of ProfileAttribute.

            param: any value, Attribute attribute, Profile profile, ProfileAttribute instance 
            return: ProfileAttribute
            exceptions: ValidationError, NotFound
        """
        serializer = ProfileAttributeSerializer(data={'value': value}, instance=instance)
        serializer.is_valid(raise_exception=True)
        return serializer.save(attribute=attribute, profile=profile)