from django.test.runner import DiscoverRunner
from django.db import connections

class CustomTestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        for conn in connections.all():
            conn.close()
        return super().teardown_databases(old_config, **kwargs)