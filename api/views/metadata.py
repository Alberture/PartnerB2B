from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from ..models import Attribute
from ..serializers import AttributeSerializer
from ..utils import valid_response

from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiResponse

class Metadata(APIView):
    """
        ViewSet that lists all Attributes.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=OpenApiResponse(
            response=inline_serializer(
                name="CreateProfileResponse",
                fields={
                    "data": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Exemple create Profile",
                    value={
                        "data": {
                            "personal data": [
                            {
                                "pk": 8,
                                "name": "firstname",
                                "displayedName": "Nom",
                                "type": "string",
                                "isRequired": True,
                                "validation": None,
                                "sensitiveData": False,
                                "attributechoice_set": []
                            },
                            {
                                "pk": 10,
                                "name": "gender",
                                "displayedName": "Genre",
                                "type": "choice",
                                "isRequired": True,
                                "validation": "unique choice",
                                "sensitiveData": False,
                                "attributechoice_set": [
                                {"displayedName": "M"},
                                {"displayedName": "F"},
                                {"displayedName": "Autre"}
                                ]
                            },
                            ],
                            "documents": [
                            {
                                "pk": 14,
                                "name": "bank_statement",
                                "displayedName": "Relevé bancaire",
                                "type": "file",
                                "isRequired": False,
                                "validation": None,
                                "sensitiveData": True,
                                "attributechoice_set": []
                            },
                            {
                                "pk": 15,
                                "name": "proof_of_address",
                                "displayedName": "Justificatif de domicile",
                                "type": "file",
                                "isRequired": False,
                                "validation": None,
                                "sensitiveData": True,
                                "attributechoice_set": []
                            }
                            ],
                        },
                        "meta": {
                            "timestamp": "2025-05-12T12:54:48.243039"
                        }
                    },
                    response_only=True
                )
            ]
        )
    )
    def get(self, request, *args, **kwargs):
        categories = Attribute.objects.values('category').distinct()
        result = {}
        for categorie in categories:
            attributes = Attribute.objects.filter(category=categorie['category'])
            serializer = AttributeSerializer(attributes, many=True)
            result[categorie['category']] = serializer.data
        
        return valid_response(result)

        