from django.apps import apps
from django.test import TestCase
from coursebuilder.apps import coursebuilderConfig


class coursebuilderConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(coursebuilderConfig.name, 'coursebuilder')
        self.assertEqual(apps.get_app_config('coursebuilder').name,
                         'coursebuilder')
