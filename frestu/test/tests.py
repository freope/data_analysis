import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))
from frestu.test.agent.trader.position_size_calculation.position_size_calculator_uniform_tests import PositionSizeCalculatorUniformTests
from frestu.test.agent.trader.position_size_calculation.position_size_calculator_linear_tests import PositionSizeCalculatorLinearTests
from frestu.test.agent.trader.probability_calculation.probability_calculator_uniform_tests import ProbabilityCalculatorUniformTests
from frestu.test.agent.trader.probability_calculation.probability_calculator_slope_ma_tests import ProbabilityCalculatorSlopeMaTests
from frestu.test.agent.trader.probability_calculation.probability_calculator_ma_slope_ma_tests import ProbabilityCalculatorMaSlopeMaTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_with_and_tests import StrategyCombinatorWithAndTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_with_or_tests import StrategyCombinatorWithOrTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_open_and_close_tests import StrategyCombinatorOpenAndCloseTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_early_close_tests import StrategyCombinatorEarlyCloseTests
from frestu.test.agent.trader.strategy.combination.strategy_combinator_simultaneous_open_tests import StrategyCombinatorSimultaneousOpenTests
from frestu.test.agent.trader.strategy.construction.oscillator.strategy_macd_reverse_stop_loss_ratio_tests import StrategyMacdReverseStopLossRatioTests
from frestu.test.agent.trader.strategy.construction.trend.strategy_gcdc_and_mau_tests import StrategyGcdcAndMauTests
from frestu.test.agent.trader.strategy.construction.trend.strategy_gcdc_stop_loss_ratio_tests import StrategyGcdcStopLossRatioTests
from frestu.test.agent.trader.strategy.construction.trend.strategy_ha_bb_mas_mstd_mss_tests import StrategyHaBbMasMstdMssTests
from frestu.test.agent.trader.strategy.construction.trend.strategy_ha_bb_mas_mstd_tests import StrategyHaBbMasMstdTests
from frestu.test.agent.trader.strategy.cross.strategy_cross_indicator_raw_tests import StrategyCrossIndicatorRawTests
from frestu.test.agent.trader.strategy.cross.strategy_cross_indicators_already_calculated_tests import StrategyCrossIndicatorsAlreadyCalculatedTests
from frestu.test.agent.trader.strategy.cross.strategy_cross_indicators_tests import StrategyCrossIndicatorsTests
from frestu.test.agent.trader.strategy.cross.strategy_dbma_bounded_tests import StrategyDbmaBoundedTests
from frestu.test.agent.trader.strategy.cross.strategy_dbma_raw_tests import StrategyDbmaRawTests
from frestu.test.agent.trader.strategy.cross.strategy_dbma_reverse_tests import StrategyDbmaReverseTests
from frestu.test.agent.trader.strategy.cross.strategy_dbma_tests import StrategyDbmaTests
from frestu.test.agent.trader.strategy.cross.strategy_dfma_bounded_tests import StrategyDfmaBoundedTests
from frestu.test.agent.trader.strategy.cross.strategy_dfma_tests import StrategyDfmaTests
from frestu.test.agent.trader.strategy.oscillator.strategy_deviation_rate_tests import StrategyDeviationRateTests
from frestu.test.agent.trader.strategy.oscillator.strategy_rsi_tests import StrategyRsiTests
from frestu.test.agent.trader.strategy.oscillator.strategy_macd_tests import StrategyMacdTests
from frestu.test.agent.trader.strategy.oscillator.strategy_madc_tests import StrategyMadcTests
from frestu.test.agent.trader.strategy.oscillator.strategy_osci_tests import StrategyOsciTests
from frestu.test.agent.trader.strategy.oscillator.strategy_fast_stochastics_tests import StrategyFastStochasticsTests
from frestu.test.agent.trader.strategy.oscillator.strategy_slow_stochastics_tests import StrategySlowStochasticsTests
from frestu.test.agent.trader.strategy.oscillator.strategy_cci_tests import StrategyCciTests
from frestu.test.agent.trader.strategy.oscillator.strategy_dmi_di_tests import StrategyDmiDiTests
from frestu.test.agent.trader.strategy.oscillator.strategy_dmi_di_adx_tests import StrategyDmiDiAdxTests
from frestu.test.agent.trader.strategy.part.strategy_part_stop_loss_tests import StrategyPartStopLossTests
from frestu.test.agent.trader.strategy.part.strategy_part_stop_loss_ratio_tests import StrategyPartStopLossRatioTests
from frestu.test.agent.trader.strategy.part.strategy_part_take_profit_tests import StrategyPartTakeProfitTests
from frestu.test.agent.trader.strategy.part.strategy_part_take_profit_ratio_tests import StrategyPartTakeProfitRatioTests
from frestu.test.agent.trader.strategy.period.strategy_regular_interval_and_curvature_tests import StrategyRegularIntervalAndCurvatureTests
from frestu.test.agent.trader.strategy.period.strategy_regular_interval_and_slope_tests import StrategyRegularIntervalAndSlopeTests
from frestu.test.agent.trader.strategy.period.strategy_regular_interval_tests import StrategyRegularIntervalTests
from frestu.test.agent.trader.strategy.regression.strategy_cross_lasso_raw_skip_tests import StrategyCrossLassoRawSkipTests
from frestu.test.agent.trader.strategy.regression.strategy_cross_lasso_raw_tests import StrategyCrossLassoRawTests
from frestu.test.agent.trader.strategy.regression.strategy_cross_ridge_raw_gev_tests import StrategyCrossRidgeRawGevTests
from frestu.test.agent.trader.strategy.regression.strategy_cross_ridge_raw_skip_tests import StrategyCrossRidgeRawSkipTests
from frestu.test.agent.trader.strategy.regression.strategy_cross_ridge_raw_tests import StrategyCrossRidgeRawTests
from frestu.test.agent.trader.strategy.stochastic_process.strategy_local_level_cross_filter_smooth_tests import StrategyLocalLevelCrossFilterSmoothTests
from frestu.test.agent.trader.strategy.stochastic_process.strategy_local_level_cross_smooths_tests import StrategyLocalLevelCrossSmoothsTests
from frestu.test.agent.trader.strategy.stochastic_process.strategy_local_level_cross_raw_filter_tests import StrategyLocalLevelCrossRawFilterTests
from frestu.test.agent.trader.strategy.trend.strategy_bb_masm_mstd_mssm_tests import StrategyBbMasmMstdMssmTests
from frestu.test.agent.trader.strategy.trend.strategy_bb_masm_mstd_tests import StrategyBbMasmMstdTests
from frestu.test.agent.trader.strategy.trend.strategy_bb_cross_ma_sigma_tests import StrategyBbCrossMaSigmaTests
from frestu.test.agent.trader.strategy.trend.strategy_gccd_tests import StrategyGccdTests
from frestu.test.agent.trader.strategy.trend.strategy_gcdc_tests import StrategyGcdcTests
from frestu.test.agent.trader.strategy.trend.strategy_heikinashi_cross_raw_ha_tests import StrategyHeikinashiCrossRawHaTests
from frestu.test.agent.trader.strategy.trend.strategy_heikinashi_tests import StrategyHeikinashiTests
from frestu.test.agent.trader.strategy.trend.strategy_mau_tests import StrategyMauTests
from frestu.test.agent.trader.strategy.trend.strategy_mau_dependent_close_tests import StrategyMauDependentCloseTests
from frestu.test.agent.trader.strategy.trend.strategy_parabolic_sar_tests import StrategyParabolicSarTests
from frestu.test.agent.trader.strategy.trend.strategy_rainbow_tests import StrategyRainbowTests
from frestu.test.agent.trader.strategy.trend.strategy_rainbow_limiting_slope_tests import StrategyRainbowLimitingSlopeTests
from frestu.test.agent.trader.trader_tests import TraderTests
from frestu.test.agent.trader.position_tests import PositionTests
from frestu.test.data_type.data_frame.data_frame_tests import DataFrameTests
from frestu.test.data_type.data_frame.data_frame_fx_tests import DataFrameFxTests
from frestu.test.feature_extraction.time_series.extractor_heikinashi_tests import ExtractorHeikinashiTests
from frestu.test.feature_extraction.time_series.extractor_parabolic_sar_tests import ExtractorParabolicSarTests
from frestu.test.feature_extraction.time_series.prediction.builder_feature_tests import BuilderFeatureTests
from frestu.test.feature_extraction.time_series.prediction.extractor_prediction_iterable_tests import ExtractorPredictionIterableTests
from frestu.test.feature_extraction.time_series.prediction.extractor_prediction_tests import ExtractorPredictionTests
from frestu.test.feature_extraction.time_series.spectrum.extractor_fft_tests import ExtractorFftTests
from frestu.test.feature_extraction.time_series.spectrum.extractor_spectrum_ma_tests import ExtractorSpectrumMaTests
from frestu.test.feature_extraction.time_series.spectrum.extractor_spectrums_peak_ma_tests import ExtractorSpectrumsPeakMaTests
from frestu.test.feature_extraction.time_series.spectrum.extractor_stft_tests import ExtractorStftTests
from frestu.test.feature_extraction.time_series.spectrum.extractor_wavelet_tests import ExtractorWaveletTests
from frestu.test.feature_extraction.time_series.stochastic_process.extractor_local_level_sequential_smooth_tests import ExtractorLocalLevelSequentialSmoothTests
from frestu.test.feature_extraction.time_series.stochastic_process.extractor_local_level_tests import ExtractorLocalLevelTests
from frestu.test.feature_extraction.time_series.extractor_making_pasts_nan_tests import ExtractorMakingPastsNanTests
from frestu.test.feature_extraction.time_series.extractor_dbma_tests import ExtractorDbmaTests
from frestu.test.feature_extraction.time_series.extractor_deviation_rate_tests import ExtractorDeviationRateTests
from frestu.test.feature_extraction.time_series.extractor_dfma_tests import ExtractorDfmaTests
from frestu.test.feature_extraction.time_series.extractor_identity_tests import ExtractorIdentityTests
from frestu.test.feature_extraction.time_series.extractor_ma_tests import ExtractorMaTests
from frestu.test.feature_extraction.time_series.extractor_mstd_tests import ExtractorMstdTests
from frestu.test.feature_extraction.time_series.extractor_ohlc_tests import ExtractorOhlcTests
from frestu.test.feature_extraction.time_series.extractor_rsi_tests import ExtractorRsiTests
from frestu.test.feature_extraction.time_series.extractor_stochastics_tests import ExtractorStochasticsTests
from frestu.test.feature_selection.selector_black_columns_tests import SelectorBlackColumnsTests
from frestu.test.feature_selection.selector_each_column_tests import SelectorEachColumnTests
from frestu.test.feature_selection.selector_identity_tests import SelectorIdentityTests
from frestu.test.feature_selection.selector_white_columns_tests import SelectorWhiteColumnsTests
from frestu.test.model_selection.split_data_frame.splitter_index_tests import SplitterIndexTests
from frestu.test.model_selection.split_data_frame.splitter_number_tests import SplitterNumberTests
from frestu.test.model_selection.split_data_frame.splitter_percentage_tests import SplitterPercentageTests
from frestu.test.model_selection.split_data_frame.splitter_time_series_constant_tests import SplitterTimeSeriesConstantTests
from frestu.test.optimization.agent.trader.strategy.period.spectrum.optimizer_strategy_regular_interval_tests import OptimizerStrategyRegularIntervalTests
from frestu.test.optimization.ga.gene.gene_discrete_tests import GeneDiscreteTests
from frestu.test.optimization.ga.gene.gene_continuous_tests import GeneContinuousTests
from frestu.test.optimization.ga.gene.gene_continuous_logscale_tests import GeneContinuousLogscaleTests
from frestu.test.optimization.ga.population_tests import PopulationTests
from frestu.test.optimization.ga.individual_tests import IndividualTests
from frestu.test.optimization.ga.crossover_tests import CrossoverTests
from frestu.test.optimization.ga.selection_tests import SelectionTests
from frestu.test.validation.span_maker_tests import SpanMakerTests


def test_suite():
    """
    builds the test suite.
    """
    suite = unittest.TestSuite()

    # position_size_calculation
    suite.addTests(unittest.makeSuite(PositionSizeCalculatorUniformTests))
    suite.addTests(unittest.makeSuite(PositionSizeCalculatorLinearTests))

    # probability_calculation
    suite.addTests(unittest.makeSuite(ProbabilityCalculatorUniformTests))
    suite.addTests(unittest.makeSuite(ProbabilityCalculatorSlopeMaTests))
    suite.addTests(unittest.makeSuite(ProbabilityCalculatorMaSlopeMaTests))

    # trader
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
    suite.addTests(unittest.makeSuite(StrategyGcdcAndMauTests))
    suite.addTests(unittest.makeSuite(StrategyGcdcStopLossRatioTests))
    suite.addTests(unittest.makeSuite(StrategyHaBbMasMstdMssTests))
    suite.addTests(unittest.makeSuite(StrategyHaBbMasMstdTests))
    suite.addTests(unittest.makeSuite(StrategyMacdReverseStopLossRatioTests))
    # cross
    suite.addTests(unittest.makeSuite(StrategyCrossIndicatorRawTests))
    suite.addTests(unittest.makeSuite(StrategyCrossIndicatorsAlreadyCalculatedTests))
    suite.addTests(unittest.makeSuite(StrategyCrossIndicatorsTests))
    suite.addTests(unittest.makeSuite(StrategyDbmaBoundedTests))
    suite.addTests(unittest.makeSuite(StrategyDbmaRawTests))
    suite.addTests(unittest.makeSuite(StrategyDbmaReverseTests))
    suite.addTests(unittest.makeSuite(StrategyDbmaTests))
    suite.addTests(unittest.makeSuite(StrategyDfmaBoundedTests))
    suite.addTests(unittest.makeSuite(StrategyDfmaTests))
    # part
    suite.addTests(unittest.makeSuite(StrategyPartStopLossTests))
    suite.addTests(unittest.makeSuite(StrategyPartStopLossRatioTests))
    suite.addTests(unittest.makeSuite(StrategyPartTakeProfitTests))
    suite.addTests(unittest.makeSuite(StrategyPartTakeProfitRatioTests))
    # period
    suite.addTests(unittest.makeSuite(StrategyRegularIntervalAndCurvatureTests))
    suite.addTests(unittest.makeSuite(StrategyRegularIntervalAndSlopeTests))
    suite.addTests(unittest.makeSuite(StrategyRegularIntervalTests))
    # prediction
    suite.addTests(unittest.makeSuite(StrategyCrossLassoRawSkipTests))
    suite.addTests(unittest.makeSuite(StrategyCrossLassoRawTests))
    suite.addTests(unittest.makeSuite(StrategyCrossRidgeRawGevTests))
    suite.addTests(unittest.makeSuite(StrategyCrossRidgeRawSkipTests))
    suite.addTests(unittest.makeSuite(StrategyCrossRidgeRawTests))
    # stochastic_process
    # suite.addTests(unittest.makeSuite(StrategyLocalLevelCrossFilterSmoothTests))
    # suite.addTests(unittest.makeSuite(StrategyLocalLevelCrossSmoothsTests))
    # suite.addTests(unittest.makeSuite(StrategyLocalLevelCrossRawFilterTests))
    # oscillator
    suite.addTests(unittest.makeSuite(StrategyDeviationRateTests))
    suite.addTests(unittest.makeSuite(StrategyRsiTests))
    suite.addTests(unittest.makeSuite(StrategyMacdTests))
    suite.addTests(unittest.makeSuite(StrategyOsciTests))
    suite.addTests(unittest.makeSuite(StrategyFastStochasticsTests))
    suite.addTests(unittest.makeSuite(StrategySlowStochasticsTests))
    suite.addTests(unittest.makeSuite(StrategyCciTests))
    suite.addTests(unittest.makeSuite(StrategyDmiDiTests))
    suite.addTests(unittest.makeSuite(StrategyDmiDiAdxTests))
    # trend
    suite.addTests(unittest.makeSuite(StrategyBbMasmMstdMssmTests))
    suite.addTests(unittest.makeSuite(StrategyBbMasmMstdTests))
    suite.addTests(unittest.makeSuite(StrategyBbCrossMaSigmaTests))
    suite.addTests(unittest.makeSuite(StrategyGccdTests))
    suite.addTests(unittest.makeSuite(StrategyGcdcTests))
    suite.addTests(unittest.makeSuite(StrategyHeikinashiCrossRawHaTests))
    suite.addTests(unittest.makeSuite(StrategyHeikinashiTests))
    suite.addTests(unittest.makeSuite(StrategyMadcTests))    
    suite.addTests(unittest.makeSuite(StrategyMauDependentCloseTests))
    suite.addTests(unittest.makeSuite(StrategyMauTests))
    suite.addTests(unittest.makeSuite(StrategyParabolicSarTests))
    suite.addTests(unittest.makeSuite(StrategyRainbowTests))
    suite.addTests(unittest.makeSuite(StrategyRainbowLimitingSlopeTests))
    
    # data_type
    suite.addTests(unittest.makeSuite(DataFrameTests))
    suite.addTests(unittest.makeSuite(DataFrameFxTests))

    # feature_extraction
    suite.addTests(unittest.makeSuite(ExtractorHeikinashiTests))
    suite.addTests(unittest.makeSuite(ExtractorParabolicSarTests))
    suite.addTests(unittest.makeSuite(BuilderFeatureTests))
    suite.addTests(unittest.makeSuite(ExtractorPredictionIterableTests))
    suite.addTests(unittest.makeSuite(ExtractorPredictionTests))
    suite.addTests(unittest.makeSuite(ExtractorFftTests))
    suite.addTests(unittest.makeSuite(ExtractorSpectrumMaTests))
    suite.addTests(unittest.makeSuite(ExtractorSpectrumsPeakMaTests))
    suite.addTests(unittest.makeSuite(ExtractorStftTests))
    suite.addTests(unittest.makeSuite(ExtractorWaveletTests))
    # suite.addTests(unittest.makeSuite(ExtractorLocalLevelSequentialSmoothTests))
    # suite.addTests(unittest.makeSuite(ExtractorLocalLevelTests))
    suite.addTests(unittest.makeSuite(ExtractorMakingPastsNanTests))
    suite.addTests(unittest.makeSuite(ExtractorDbmaTests))
    suite.addTests(unittest.makeSuite(ExtractorDeviationRateTests))
    suite.addTests(unittest.makeSuite(ExtractorDfmaTests))
    suite.addTests(unittest.makeSuite(ExtractorIdentityTests))
    suite.addTests(unittest.makeSuite(ExtractorMaTests))
    suite.addTests(unittest.makeSuite(ExtractorMstdTests))
    suite.addTests(unittest.makeSuite(ExtractorOhlcTests))
    suite.addTests(unittest.makeSuite(ExtractorRsiTests))
    suite.addTests(unittest.makeSuite(ExtractorStochasticsTests))

    # feature_selection
    suite.addTests(unittest.makeSuite(SelectorBlackColumnsTests))
    suite.addTests(unittest.makeSuite(SelectorEachColumnTests))
    suite.addTests(unittest.makeSuite(SelectorIdentityTests))
    suite.addTests(unittest.makeSuite(SelectorWhiteColumnsTests))

    # model_selection
    suite.addTests(unittest.makeSuite(SplitterIndexTests))
    suite.addTests(unittest.makeSuite(SplitterNumberTests))
    suite.addTests(unittest.makeSuite(SplitterPercentageTests))
    suite.addTests(unittest.makeSuite(SplitterTimeSeriesConstantTests))

    # optimization
    suite.addTests(unittest.makeSuite(OptimizerStrategyRegularIntervalTests))
    suite.addTests(unittest.makeSuite(GeneDiscreteTests))
    suite.addTests(unittest.makeSuite(GeneContinuousTests))
    suite.addTests(unittest.makeSuite(GeneContinuousLogscaleTests))
    suite.addTests(unittest.makeSuite(PopulationTests))
    suite.addTests(unittest.makeSuite(IndividualTests))
    suite.addTests(unittest.makeSuite(CrossoverTests))
    suite.addTests(unittest.makeSuite(SelectionTests))

    # validation
    suite.addTests(unittest.makeSuite(SpanMakerTests))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')