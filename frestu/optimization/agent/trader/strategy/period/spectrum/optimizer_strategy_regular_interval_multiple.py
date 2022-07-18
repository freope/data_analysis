import numpy as np
import pandas as pd

from frestu.feature_extraction.time_series.spectrum import ExtractorSpectrumsPeakMa
from frestu.optimization.agent.trader.strategy.period.spectrum import OptimizerStrategyRegularInterval as OptimizerParent


class OptimizerStrategyRegularIntervalMultiple(OptimizerParent):
    
    def __init__(self, windows, params_default):
        super().__init__(windows, None)
        self.__params_default = params_default

    def _calculate_the_best_params(self, features):
        # 周期の候補を計算
        periods_half = self._calculate_periods_candidate(features)

        # 周期の候補それぞれの最良の適合度と offset を計算
        offsets, fitnesses = self._calculate_offsets_candidate(periods_half)

        if len(fitnesses) == 0:
            return self.__params_default

        params = {
            'periods_half': periods_half,
            'offsets': offsets,
        }
        
        # パラメータを self.evaluate に直接渡せる形に適合させる。
        params = self._adapt_params_to_evaluate(params)

        return params

    @classmethod
    def calculate_offsets_test(cls, periods_half, offsets_train, n_rows_train):
        offsets_test = [
            cls.calculate_offset_test(period_half, offset_train, n_rows_train)
            for period_half, offset_train in zip(periods_half, offsets_train)
        ]
        return offsets_test