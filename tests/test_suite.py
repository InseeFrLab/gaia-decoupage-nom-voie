import unittest
from finders_test.find_complement_test.complement_finder_test import ComplementFinderTest

import sys

# cd tests
# python test_suite.py

src_path = "../src/decoupage_libelles/"
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Test archi
    suite.addTest(loader.loadTestsFromTestCase(ComplementFinderTest))
