from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ..utils import get_authenticated_partner, get_profile_or_error, get_attribute_or_error, process_attribute_value, error_response

from ..serializers import ProfileSerializer, ProfileItemSerializer, ProfileAttributeDocumentSerializer
from ..models import Profile, ProfileAttribute, Attribute


class ProfileViewSet(ModelViewSet):
    """
    ViewSet for Profile management (CRUD)
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        partner = get_authenticated_partner(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(partner=partner)
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = get_attribute_or_error(name)
                if not attribute:
                    return error_response(f"L'attribut {name} n'existe pas.")

                if not process_attribute_value(value, attribute, profile):
                    return error_response("Le format des données n'est pas respecté")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return error_response("Le format des données n'est pas respecté")

    def retrieve(self, request, pk, *args, **kwargs):
        partner = get_authenticated_partner(request)
        profile = get_profile_or_error(pk, partner)
        
        if not profile:
            return error_response("Ce profil n'existe pas. Veuillez vérifier l'identifiant de l'utilisateur.")

        serializer = ProfileItemSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, pk, *args, **kwargs):
        partner = get_authenticated_partner()
        profile = get_profile_or_error(pk, partner)
        if not profile:
            return error_response("Ce profil n'existe pas. Veuillez vérifier l'identifiant de l'utilisateur.")

        serializer = self.get_serializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = get_attribute_or_error(name)
                if not attribute:
                    return error_response(f"L'attribut {name} n'existe pas.")

                profile_attribute_qs = ProfileAttribute.objects.filter(profile=profile, attribute=attribute)

                if isinstance(value, list):
                    profile_attribute_qs.delete()

                if not process_attribute_value(value, attribute, profile, profile_attribute_qs.first()):
                    return error_response("Le format des données n'est pas respecté")

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        partner = get_authenticated_partner(request)
        profile = get_profile_or_error(pk, partner)
        if not profile:
            return error_response("Nous n'avons pas pu trouver ce profil. Veuillez vérifier l'identifiant de l'utilisateur.")

        profile.status = 'complete'
        profile.save()

        return Response({
            'status': 'Complet',
            'message': 'Ce profil a été marqué comme complet et prêt pour analyse.'
        })
    
    def destroy(self, request, *args, **kwargs):
        return error_response('Not allowed to DELETE')
    
    def update(self, request, *args, **kwargs):
        return error_response('Not allowed to PUT')

    def list(self, request, *args, **kwargs):
        return error_response('Not allowed to GET')


    