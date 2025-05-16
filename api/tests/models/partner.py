from django.test import TestCase

from api.models import Partner

class PartnerTestCase(TestCase):
    def setUp(self):
        Partner.objects.create(name="admin", limitUsage=4)
        Partner.objects.create(name="banque", limitUsage=0)
        
    def test_initial_activation_status_is_pending(self):
        admin = Partner.objects.get(name="admin")
        bank = Partner.objects.get(name="banque")
        self.assertEqual(admin.activationStatus, 'pending')
        self.assertEqual(bank.activationStatus, 'pending')

    def test_limit_usage_value(self):
        admin = Partner.objects.get(name="admin")
        bank = Partner.objects.get(name="banque")
        self.assertEqual(admin.limitUsage, 4)
        self.assertEqual(bank.limitUsage, 0)

    def test_api_key_is_not_null(self):
        admin = Partner.objects.get(name="admin")
        bank = Partner.objects.get(name="banque")
        self.assertIsNotNone(admin.apiKey)
        self.assertIsNotNone(bank.apiKey)
    