import os
import sys
import unittest

def run():
    tests = unittest.TestLoader().discover('.')
    passed = unittest.TextTestRunner().run(tests).wasSuccessful()

    sys.exit(0 if passed else 1)
