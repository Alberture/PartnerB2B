from django.test import TestCase

from api.models import Attribute

class AttributeTestCase(TestCase):
    def setUp(self):
        Attribute.objects.create(name="firstname", displayedName="prénom", type="string", category="personal data", isRequired=True,sensitiveData=False)
        Attribute.objects.create(name="lastname", displayedName="nom", type="string", category="personal data", isRequired=True,sensitiveData=False)
        Attribute.objects.create(name="birth_date", displayedName="Date de naissance", type="date", category="personal data", isRequired=False,sensitiveData=False)
        
    def test_is_required(self):
        firstname_attribute = Attribute.objects.get(pk=1)
        lastname_attribute = Attribute.objects.get(name="lastname")
        birth_date_attribute = Attribute.objects.get(name="birth_date")
        
        self.assertTrue(firstname_attribute.isRequired)
        self.assertTrue(lastname_attribute.isRequired)
        self.assertFalse(birth_date_attribute.isRequired)
