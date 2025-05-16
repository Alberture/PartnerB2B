from django.test import TestCase

from api.models import Profile

class ProfileTestCase(TestCase):
    def setUp(self):
        Profile.objects.create()
        Profile.objects.create(externalReference="ref")
        
    def test_attribute_external_value(self):
        profile1 = Profile.objects.get(pk=1)
        profile2 = Profile.objects.get(pk=2)
        
        self.assertIsNone(profile1.externalReference)
        self.assertEqual(profile2.externalReference, "ref")