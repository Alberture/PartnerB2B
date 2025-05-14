from rest_framework.viewsets import ModelViewSet
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import MethodNotAllowed, ValidationError

from ..utils import valid_response

from ..serializers import ProfileSerializer, ProfileItemSerializer, ProfileAttributeSerializer, ProfileAttributeDocumentSerializer, AnalysisSerializer
from ..models import Profile, ProfileAttribute, Attribute, Partner
from ..permissions import ProfileBelongsToPartner, IsAdminOrHasEnoughTries, UpdateAndListNotAllowed

from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view

from datetime import datetime

@extend_schema_view(
    list=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
)
class ProfileViewSet(ModelViewSet):
    """
        ViewSet that manages Profile objects.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        IsAuthenticated, 
        ProfileBelongsToPartner,
        IsAdminOrHasEnoughTries,
        UpdateAndListNotAllowed
    ]
    parser_classes = [MultiPartParser, FormParser, JSONParser, ]

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
            name="Exemple create Analysis",
            value={
                "data": {
                    "message": "Vous venez de faire une demande d'analyse pour le profile 297",
                    "pk": 13,
                    "status": "pending"
                },
                "meta": {
                    "timestamp": "2025-05-12T12:04:24.219023"
                }
            },
            response_only=True
            )
        ],
        responses=AnalysisSerializer,
    )
    @action(detail=True, methods=['post'], url_path='analyses')
    def create_analysis(self, request, pk=None):
        profile = self.get_object()
        serializer = AnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        analysis = serializer.save(profile=profile)
        partner = Partner.get_authenticated_partner(request)
        if partner.limitUsage:
            partner.limitUsage -= 1
            partner.save()
        return valid_response({
            'message': "Vous venez de faire une demande d\'analyse pour le profile %s" % (pk),
            'pk': analysis.id,
            'status': analysis.status   
        }, request.id, code=status.HTTP_201_CREATED)
    
    @extend_schema(
        request=ProfileAttributeDocumentSerializer,
        examples=[
            OpenApiExample(
            name="Exemple create Document",
            value={
                "data": {
                    "pk": 13,
                    "status": "pending",
                    "downloadedAt": "2025-05-12T12:10:37.486892Z",
                    "type": "png"
                },
                "meta": {
                    "timestamp": "2025-05-12T12:10:37.538076"
                }
            },
            response_only=True
            )
        ],
        responses=ProfileAttributeDocumentSerializer
    )
    @action(detail=True, methods=['post'], url_path='documents')
    def create_document(self, request, pk=None):
        profile = self.get_object()
        serializer = ProfileAttributeDocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_attribute = Attribute.get_attribute_or_error(request.data['attribute'])
            if document_attribute.category != 'documents':
                document_attributes = Attribute.objects.filter(category="documents")
                raise ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Erreur de validation",
                    "details":[
                        { 
                            "field": "attribute",
                            "error": "L'attribute selectionnée doit faire parti de la famille des documents. Liste des attributs dans cette catégorie : %s" % (list(map(str,document_attributes)))
                        }
                    ]
                })
            type=str(request.data['file'])[str(request.data['file']).find(".")+1:]
            serializer.save(attribute=document_attribute, profile=profile, type=type)
            return valid_response(serializer.data, request.id, status.HTTP_201_CREATED)

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

    @extend_schema(
        examples=[
            OpenApiExample(
            name="Example delete Profile",
            value={
                "data": {
                    "message": "Le profil à bien été supprimé."
                },
                "meta": {
                    "timestamp": "2025-05-14T07:31:59.463958",
                    "request_id": "cd21c104-756b-44a2-b5f0-f25bccd7cb0a"
                }
            },
            response_only=True
            )
        ],
        responses=200
    )
    def destroy(self, request, pk, *args, **kwargs):
        super().destroy(request, pk, *args, **kwargs)
        return valid_response({
            "message": "Le profil à bien été supprimé.",
        }, request.id)

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