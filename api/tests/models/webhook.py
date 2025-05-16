from django.test import TestCase

from api.models import Webhook

class WebhookTestCase(TestCase):
    def setUp(self):
        Webhook.objects.create(url="url")
        
    def test_url_value(self):
        webhook = Webhook.objects.get(pk=1)
        self.assertEqual(webhook.url, 'url')