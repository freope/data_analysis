import os, sys, unittest
sys.path.append(os.path.abspath(".."))
from frestu.test.preprocessing.data_frame import DataFrameTests
from frestu.test.preprocessing.data_frame_fx import DataFrameFxTests


def test_suite():
    '''builds the test suite.'''
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(DataFrameTests))
    suite.addTests(unittest.makeSuite(DataFrameFxTests))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')