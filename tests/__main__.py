import os
import sys
import unittest
import django


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
    django.setup()
    loader = unittest.TestLoader()
    if len(sys.argv) > 1:
        suite = loader.loadTestsFromName(sys.argv[1])
    else:
        suite = loader.discover(TEST_DIR)
    runner = unittest.TextTestRunner()
    runner.run(suite)
