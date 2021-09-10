import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.tests.data_type.data_frame.data_frame_tests import DataFrameTests
from frestu.tests.data_type.data_frame.data_frame_fx_tests import DataFrameFxTests
from frestu.tests.optimization.ga.gene.gene_discrete_tests import GeneDiscreteTests
from frestu.tests.optimization.ga.gene.gene_continuous_tests import GeneContinuousTests
from frestu.tests.optimization.ga.gene.gene_continuous_logscale_tests import GeneContinuousLogscaleTests
from frestu.tests.optimization.ga.population_tests import PopulationTests
from frestu.tests.optimization.ga.individual_tests import IndividualTests
from frestu.tests.optimization.ga.crossover_tests import CrossoverTests
from frestu.tests.optimization.ga.selection_tests import SelectionTests
from frestu.tests.optimization.ga.evaluation.evaluator_regression_tests import EvaluatorRegressionTests
from frestu.tests.optimization.ga.evaluation.evaluator_classification_tests import EvaluatorClassificationTests
from frestu.tests.model_selection.train_test_split_tests import TrainTestSplitTests


def test_suite():
    '''builds the test suite.'''
    suite = unittest.TestSuite()

    # data_type
    suite.addTests(unittest.makeSuite(DataFrameTests))
    suite.addTests(unittest.makeSuite(DataFrameFxTests))

    # optimization
    suite.addTests(unittest.makeSuite(GeneDiscreteTests))
    suite.addTests(unittest.makeSuite(GeneContinuousTests))
    suite.addTests(unittest.makeSuite(GeneContinuousLogscaleTests))
    suite.addTests(unittest.makeSuite(PopulationTests))
    suite.addTests(unittest.makeSuite(IndividualTests))
    suite.addTests(unittest.makeSuite(CrossoverTests))
    suite.addTests(unittest.makeSuite(SelectionTests))
    suite.addTests(unittest.makeSuite(EvaluatorRegressionTests))
    suite.addTests(unittest.makeSuite(EvaluatorClassificationTests))

    # model_selection
    suite.addTests(unittest.makeSuite(TrainTestSplitTests))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')