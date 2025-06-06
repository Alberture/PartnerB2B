from ..models import Profile
from ..models.attribute import Attribute, AttributeChoice
from .profile_attribute import ProfileAttributeItemSerializer
from .profile_attribute_document import ProfileAttributeDocumentItemSerializer

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

class ProfileItemSerializer(serializers.ModelSerializer):
    """
        Serializer to transform a Profile object to JSON.
        Used to represent a Profile when retrieved.
    """
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    externalReference = serializers.CharField(read_only=True)
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    document_set = ProfileAttributeDocumentItemSerializer(read_only=True, many=True)
    last_analyse = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'createdAt',
            'updatedAt',
            'status',
            'externalReference',
            'profileattribute_set',
            'document_set',
            'last_analyse'
        ]

    def get_last_analyse(self, obj):
        """
            Method to retrieve the last Analysis of a Profile.
        """
        analyse = obj.analysis_set.order_by('-id')[:1].first()
        if analyse:
            return {
                'score' : analyse.score,
                'status' : analyse.status,
                'details' : analyse.details,
                'version' : analyse.version
            }
        return None
    

class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer to transform JSON to a Profile object.
        Used to create a Profile with the given data.
    """
    attributes = serializers.DictField(write_only=True)
    profileattribute_set = ProfileAttributeItemSerializer(read_only=True, many=True)
    status = serializers.CharField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    externalReference = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            'pk',
            'status',
            'createdAt',
            'profileattribute_set',
            'externalReference',
            'attributes'
        ]

    def create(self, validated_data):
        validated_data.pop("attributes")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.externalReference = validated_data.get('externalReference', instance.externalReference)
        return instance
    
    def validate(self, data):
        data = super().validate(data)
        """
            Verifies if the choices and attributes are correct. 
            If so then it retrieves all the attributes required
            based on choices made.
        """
        required_attributes = list(Attribute.objects.filter(isRequired=True).exclude(category="document"))

        if data.get('attributes') != None:
            
            for name, value in data['attributes'].items():
                attribute = Attribute.get_attribute_or_error(name=name) 
                if attribute.type == "choice":
                    if attribute.validation == 'unique choice':
                        self.check_unique_choice_validation(attribute, value)
                    if isinstance(value, list):
                        for choice in value:
                            self.value_is_in_attribute_choice_set_or_error(attribute, choice)
                            attribute_choice = AttributeChoice.get_attribute_choice_or_error(displayedName=choice)
                            required_attribute = attribute_choice.get_required_attribute_if_chosen()    
                            if required_attribute:
                                required_attributes.append(required_attribute)   
                    else:
                        self.value_is_in_attribute_choice_set_or_error(attribute, value)
                        attribute_choice = AttributeChoice.get_attribute_choice_or_error(displayedName=value)
                        required_attribute = attribute_choice.get_required_attribute_if_chosen()    
                        if required_attribute:
                            required_attributes.append(required_attribute)   

            if not self.instance:
                #Verifies if all the required attributes were set.
                required_attributes = [attribute for attribute in required_attributes if attribute.name not in data['attributes'].keys()]
                if required_attributes:
                    missing_attributes = (list(map(str, required_attributes)))
                    raise serializers.ValidationError({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing required attributes.",
                        "details":[
                            {"error": "The following attributes are missing : %s" % missing_attributes}
                        ]
                    })

            return data
        else:
            missing_attributes = Attribute.objects.filter(isRequired=True)
            raise serializers.ValidationError({
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Missing required attributes.",
                    "details":[
                        {"error": "The following attributes are missing : %s" % (list(map(str, missing_attributes)))}
                    ]
                })
    
    def value_is_in_attribute_choice_set_or_error(self, attribute, value):
        """
            Method that verifies if a value is in the attribute choice set,
            if not raises a ValidationError.

            param: Attribute attribute, any value
            exceptions: ValidationError
        """
        exists = attribute.attributechoice_set.order_by("displayedName").filter(displayedName=value)
        if not exists:
            raise serializers.ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Choice does not exist.",
                "details":[
                    {
                        "field": "value",
                        "attribute": attribute.name,
                        "error": "The choice must among : %s" % (list(map(str, attribute.attributechoice_set.order_by('displayedName')))),
                    }
                ]
            })
    
    def check_unique_choice_validation(self, attribute, value):
        """
            Method that verifies for an attribute with unique choice 
            if the choice made is unique.

            param: Attribute attribute, any value
            exceptions: ValidationError
        """
        if isinstance(value, list) and len(value) != 1:
            raise serializers.ValidationError({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Choice must be unique",
                "details":[
                    {
                        "field": "value",
                        "attribute": attribute.name,
                        "error": "The choice must be unique among : %s" % (list(map(str, attribute.attributechoice_set.order_by('displayedName')))),
                    }
                ]
            })