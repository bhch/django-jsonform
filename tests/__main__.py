import os
import unittest


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR)
    runner = unittest.TextTestRunner()
    runner.run(suite)
