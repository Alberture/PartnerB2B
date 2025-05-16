from django.test import TestCase

from api.models import Analysis

class AnalysisTestCase(TestCase):
    def setUp(self):
        Analysis.objects.create()
    
    def test_initial_status_is_pending(self):
        analysis = Analysis.objects.get(pk=1)
        self.assertEqual(analysis.status, 'pending')

    def test_init_score_details_version_null(self):
        analysis = Analysis.objects.get(pk=1)
        self.assertIsNone(analysis.score)
        self.assertIsNone(analysis.details)
        self.assertIsNone(analysis.version)
