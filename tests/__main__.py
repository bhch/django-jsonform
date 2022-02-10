import os
import unittest
import django
import django_settings


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
    django.setup()
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR)
    runner = unittest.TextTestRunner()
    runner.run(suite)
