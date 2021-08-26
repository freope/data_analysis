import os
import sys
import unittest
sys.path.append(os.path.abspath(".."))
from frestu.tests.preprocessing.data_frame_tests import DataFrameTests
from frestu.tests.preprocessing.data_frame_fx_tests import DataFrameFxTests


def test_suite():
    '''builds the test suite.'''
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(DataFrameTests))
    suite.addTests(unittest.makeSuite(DataFrameFxTests))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')