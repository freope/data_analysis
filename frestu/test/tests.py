import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.test.data_type.data_frame.data_frame_tests import DataFrameTests
from frestu.test.data_type.data_frame.data_frame_fx_tests import DataFrameFxTests
from frestu.test.optimization.ga.gene.gene_discrete_tests import GeneDiscreteTests
from frestu.test.optimization.ga.gene.gene_continuous_tests import GeneContinuousTests
from frestu.test.optimization.ga.gene.gene_continuous_logscale_tests import GeneContinuousLogscaleTests
from frestu.test.optimization.ga.population_tests import PopulationTests
from frestu.test.optimization.ga.individual_tests import IndividualTests
from frestu.test.optimization.ga.crossover_tests import CrossoverTests
from frestu.test.optimization.ga.selection_tests import SelectionTests
from frestu.test.optimization.ga.evaluation.evaluator_regression_tests import EvaluatorRegressionTests
from frestu.test.optimization.ga.evaluation.evaluator_classification_tests import EvaluatorClassificationTests
from frestu.test.model_selection.train_test_split_tests import TrainTestSplitTests
from frestu.test.agent.trader.trader_tests import TraderTests
from frestu.test.agent.trader.position_tests import PositionTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_with_and_tests import StrategyCombinatorWithAndTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_with_or_tests import StrategyCombinatorWithOrTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_open_and_close_tests import StrategyCombinatorOpenAndCloseTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_early_close_tests import StrategyCombinatorEarlyCloseTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_simultaneous_open_tests import StrategyCombinatorSimultaneousOpenTests
from frestu.test.agent.trader.strategy.construction.strategy_constructor_gcdc_and_mau_tests import StrategyConstructorGcdcAndMauTests
from frestu.test.agent.trader.strategy.construction.strategy_constructor_gcdc_loss_cut_tests import StrategyConstructorGcdcLossCutTests
from frestu.test.agent.trader.strategy.oscillator.strategy_deviation_rate_tests import StrategyDeviationRateTests
from frestu.test.agent.trader.strategy.oscillator.strategy_rsi_tests import StrategyRsiTests
from frestu.test.agent.trader.strategy.oscillator.strategy_macd_tests import StrategyMacdTests
from frestu.test.agent.trader.strategy.oscillator.strategy_dbma_tests import StrategyDbmaTests
from frestu.test.agent.trader.strategy.oscillator.strategy_dfma_tests import StrategyDfmaTests
from frestu.test.agent.trader.strategy.oscillator.strategy_osci_tests import StrategyOsciTests
from frestu.test.agent.trader.strategy.oscillator.strategy_fast_stochastics_tests import StrategyFastStochasticsTests
from frestu.test.agent.trader.strategy.oscillator.strategy_slow_stochastics_tests import StrategySlowStochasticsTests
from frestu.test.agent.trader.strategy.oscillator.strategy_cci_tests import StrategyCciTests
from frestu.test.agent.trader.strategy.oscillator.strategy_dmi_di_tests import StrategyDmiDiTests
from frestu.test.agent.trader.strategy.oscillator.strategy_dmi_di_adx_tests import StrategyDmiDiAdxTests
from frestu.test.agent.trader.strategy.trend.strategy_mau_tests import StrategyMauTests
from frestu.test.agent.trader.strategy.trend.strategy_mau_dependent_close_tests import StrategyMauDependentCloseTests
from frestu.test.agent.trader.strategy.trend.strategy_gcdc_tests import StrategyGcdcTests
from frestu.test.agent.trader.strategy.trend.strategy_parabolic_sar_tests import StrategyParabolicSarTests
from frestu.test.agent.trader.strategy.trend.strategy_bollinger_band_ma_std_threshold_tests import StrategyBollingerBandMaStdThresholdTests
from frestu.test.agent.trader.strategy.trend.strategy_bollinger_band_ma_std_threshold_slope_tests import StrategyBollingerBandMaStdThresholdSlopeTests
from frestu.test.agent.trader.strategy.part.strategy_part_loss_cut_tests import StrategyPartLossCutTests
from frestu.test.agent.trader.leverage_calculator.leverage_calculator_uniform_tests import LeverageCalculatorUniformTests
from frestu.test.agent.trader.leverage_calculator.leverage_calculator_linear_tests import LeverageCalculatorLinearTests
from frestu.test.agent.trader.probability_calculator.probability_calculator_uniform_tests import ProbabilityCalculatorUniformTests
from frestu.test.agent.trader.probability_calculator.probability_calculator_slope_tests import ProbabilityCalculatorSlopeTests
from frestu.test.agent.trader.probability_calculator.probability_calculator_ma_slope_tests import ProbabilityCalculatorMaSlopeTests
from frestu.test.feature_extraction.time_series.extractor_deviation_rate_tests import ExtractorDeviationRateTests
from frestu.test.feature_extraction.time_series.extractor_rsi_tests import ExtractorRsiTests
from frestu.test.feature_extraction.time_series.extractor_dbma_tests import ExtractorDbmaTests
from frestu.test.feature_extraction.time_series.extractor_dfma_tests import ExtractorDfmaTests
from frestu.test.feature_extraction.time_series.extractor_heikinashi_tests import ExtractorHeikinashiTests
from frestu.test.feature_extraction.time_series.extractor_ma_std_tests import ExtractorMaStdTests
from frestu.test.feature_extraction.time_series.extractor_parabolic_sar_tests import ExtractorParabolicSarTests
from frestu.test.feature_extraction.time_series.extractor_stochastics_tests import ExtractorStochasticsTests
from frestu.test.feature_extraction.time_series.extractor_ohlc_tests import ExtractorOhlcTests


def test_suite():
    """
    builds the test suite.
    """
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

    # agent
    suite.addTests(unittest.makeSuite(TraderTests))
    suite.addTests(unittest.makeSuite(PositionTests))

    # strategy
    # combination
    suite.addTests(unittest.makeSuite(StrategyCombinatorWithAndTests))
    suite.addTests(unittest.makeSuite(StrategyCombinatorWithOrTests))
    suite.addTests(unittest.makeSuite(StrategyCombinatorOpenAndCloseTests))
    suite.addTests(unittest.makeSuite(StrategyCombinatorEarlyCloseTests))
    suite.addTests(unittest.makeSuite(StrategyCombinatorSimultaneousOpenTests))
    # constructor
    suite.addTests(unittest.makeSuite(StrategyConstructorGcdcAndMauTests))
    suite.addTests(unittest.makeSuite(StrategyConstructorGcdcLossCutTests))
    # part
    suite.addTests(unittest.makeSuite(StrategyPartLossCutTests))
    # oscillator
    suite.addTests(unittest.makeSuite(StrategyDeviationRateTests))
    suite.addTests(unittest.makeSuite(StrategyRsiTests))
    suite.addTests(unittest.makeSuite(StrategyMacdTests))
    suite.addTests(unittest.makeSuite(StrategyDbmaTests))
    suite.addTests(unittest.makeSuite(StrategyDfmaTests))
    suite.addTests(unittest.makeSuite(StrategyOsciTests))
    suite.addTests(unittest.makeSuite(StrategyFastStochasticsTests))
    suite.addTests(unittest.makeSuite(StrategySlowStochasticsTests))
    suite.addTests(unittest.makeSuite(StrategyCciTests))
    suite.addTests(unittest.makeSuite(StrategyDmiDiTests))
    suite.addTests(unittest.makeSuite(StrategyDmiDiAdxTests))
    # trend
    suite.addTests(unittest.makeSuite(StrategyMauDependentCloseTests))
    suite.addTests(unittest.makeSuite(StrategyMauTests))
    suite.addTests(unittest.makeSuite(StrategyGcdcTests))
    suite.addTests(unittest.makeSuite(StrategyParabolicSarTests))
    suite.addTests(unittest.makeSuite(StrategyBollingerBandMaStdThresholdTests))
    suite.addTests(unittest.makeSuite(
        StrategyBollingerBandMaStdThresholdSlopeTests))

    # leverage_calculator
    suite.addTests(unittest.makeSuite(LeverageCalculatorUniformTests))
    suite.addTests(unittest.makeSuite(LeverageCalculatorLinearTests))

    # probability_calculator
    suite.addTests(unittest.makeSuite(ProbabilityCalculatorUniformTests))
    suite.addTests(unittest.makeSuite(ProbabilityCalculatorSlopeTests))
    suite.addTests(unittest.makeSuite(ProbabilityCalculatorMaSlopeTests))

    # feature_extraction
    suite.addTests(unittest.makeSuite(ExtractorDeviationRateTests))
    suite.addTests(unittest.makeSuite(ExtractorRsiTests))
    suite.addTests(unittest.makeSuite(ExtractorDbmaTests))
    suite.addTests(unittest.makeSuite(ExtractorDfmaTests))
    suite.addTests(unittest.makeSuite(ExtractorHeikinashiTests))
    suite.addTests(unittest.makeSuite(ExtractorMaStdTests))
    suite.addTests(unittest.makeSuite(ExtractorParabolicSarTests))
    suite.addTests(unittest.makeSuite(ExtractorStochasticsTests))
    suite.addTests(unittest.makeSuite(ExtractorOhlcTests))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')