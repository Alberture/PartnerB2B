from django.test import TestCase

from api.models import ProfileAttributeDocument, Profile, Attribute

class ProfileAttributeDocumentTestCase(TestCase):
    def setUp(self):
        profiles = [
            Profile.objects.create(),
            Profile.objects.create()
        ]
        attributes = [    
            Attribute.objects.create(name="bank_state", displayedName="bank_state", type="file", category="personal data", isRequired=True, sensitiveData=True),
        ]
        ProfileAttributeDocument.objects.create(profile=profiles[0], attribute=attributes[0], file="/path/image.png", type="png")
    
    def test_initial_status(self):
        document = ProfileAttributeDocument.objects.get(pk=1)
        self.assertEqual(document.status, 'pending')