from ..serializers.profile_attribute import ProfileAttributeSerializer

def save_value(value, attribute, profile, instance=None):
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