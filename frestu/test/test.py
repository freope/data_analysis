import os, sys, unittest
sys.path.append(os.path.abspath(".."))
from frestu.test.preprocessing.data_frame_frestu import DataFrameFrestuTests
from frestu.test.preprocessing.data_frame_frestu_fx import DataFrameFrestuFxTests


def test_suite():
    '''builds the test suite.'''
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(DataFrameFrestuTests))
    suite.addTests(unittest.makeSuite(DataFrameFrestuFxTests))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')