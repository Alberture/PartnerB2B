from django.test import TestCase

from api.models import ProfileAttribute, Profile, Attribute

class ProfileAttributeTestCase(TestCase):
    def setUp(self):

        profiles = [
            Profile.objects.create(),
            Profile.objects.create()
        ]

        attributes = [    
            Attribute.objects.create(name="firstname", displayedName="prénom", type="string", category="personal data", isRequired=True, sensitiveData=False),
            Attribute.objects.create(name="lastname", displayedName="nom", type="string", category="personal data", isRequired=True, sensitiveData=False),
            Attribute.objects.create(name="birth_date", displayedName="Date de naissance", type="date", isRequired=False, category="personal data", sensitiveData=False)
        ]

        ProfileAttribute.objects.create(profile=profiles[0], attribute=attributes[0], value="Jean-Luck")
        ProfileAttribute.objects.create(profile=profiles[0], attribute=attributes[1], value="Sithi")
        ProfileAttribute.objects.create(profile=profiles[0], attribute=attributes[2], value="2005-07-21")
        ProfileAttribute.objects.create(profile=profiles[1], attribute=attributes[0], value="Cyril")
        ProfileAttribute.objects.create(profile=profiles[1], attribute=attributes[1], value="Perosino")
        ProfileAttribute.objects.create(profile=profiles[1], attribute=attributes[2], value="1998-12-20")
        
    def test_attribute_number(self):
        profile1 = Profile.objects.get(pk=1)
        self.assertEqual(len(profile1.profileattribute_set.order_by("value")), 3)

    def test_values(self):
        profile1 = Profile.objects.get(pk=1)
        attributes = profile1.profileattribute_set.order_by("value")
        self.assertEqual(attributes.get(value="Jean-Luck").value, "Jean-Luck")
        self.assertEqual(attributes.get(value="Sithi").value, "Sithi")
        self.assertEqual(attributes.get(value="2005-07-21").value, "2005-07-21")
        self.assertEqual(list(attributes.filter(value="not valid")), [])
