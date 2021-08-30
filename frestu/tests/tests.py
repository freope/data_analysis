import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.tests.preprocessing.data_frame_tests import DataFrameTests
from frestu.tests.preprocessing.data_frame_fx_tests import DataFrameFxTests
from frestu.tests.optimization.ga.gene.gene_discrete_tests import GeneDiscreteTests
from frestu.tests.optimization.ga.gene.gene_continuous_tests import GeneContinuousTests
from frestu.tests.optimization.ga.gene.gene_continuous_logscale_tests import GeneContinuousLogscaleTests
from frestu.tests.optimization.ga.population_tests import PopulationTests
from frestu.tests.optimization.ga.individual_tests import IndividualTests
from frestu.tests.optimization.ga.crossover_tests import CrossoverTests
from frestu.tests.optimization.ga.selection_tests import SelectionTests


def test_suite():
    '''builds the test suite.'''
    suite = unittest.TestSuite()

    suite.addTests(unittest.makeSuite(DataFrameTests))
    suite.addTests(unittest.makeSuite(DataFrameFxTests))

    suite.addTests(unittest.makeSuite(GeneDiscreteTests))
    suite.addTests(unittest.makeSuite(GeneContinuousTests))
    suite.addTests(unittest.makeSuite(GeneContinuousLogscaleTests))
    suite.addTests(unittest.makeSuite(PopulationTests))
    suite.addTests(unittest.makeSuite(IndividualTests))
    suite.addTests(unittest.makeSuite(CrossoverTests))
    suite.addTests(unittest.makeSuite(SelectionTests))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')