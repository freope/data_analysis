import numpy as np
import pandas as pd

from frestu.feature_extraction.time_series.spectrum import ExtractorSpectrumsPeakMa
from frestu.optimization.agent.trader.strategy import OptimizerStrategyAbstract


class OptimizerStrategyRegularInterval(OptimizerStrategyAbstract):
    
    def __init__(self, windows, params_default):
        super().__init__()
        self.__windows = windows
        self.__params_default = params_default
        self.candidates = {'window': [], 'period_half': [], 'offset': []}
        self.ix_best = None
    
    def _calculate_features(self, df):
        extractor = ExtractorSpectrumsPeakMa('sma', self.__windows)
        freqs, spectrum = extractor.extract(df)
        periods = [1 / freq for freq in freqs]

        features = pd.DataFrame([self.__windows, periods, spectrum]).T
        features.columns = ['window', 'period', 'spectrum']
        features = features.set_index('window')

        return features

    def _calculate_the_best_params(self, features):
        # 周期の候補を計算
        periods_half = self._calculate_periods_candidate(features)

        # 周期の候補それぞれの最良の適合度と offset を計算
        offsets, fitnesses = self._calculate_offsets_candidate(periods_half)

        # 最良のパラメータを選択
        self.ix_best = self._select_the_best_ix(fitnesses)

        if self.ix_best is None:
            return self.__params_default

        params = {
            'period_half': periods_half[self.ix_best],
            'offset': offsets[self.ix_best],
        }
        
        # パラメータを self.evaluate に直接渡せる形に適合させる。
        params = self._adapt_params_to_evaluate(params)

        return params
    
    def _calculate_periods_candidate(self, features):
        # 傾きが非負から負に変わる箇所が候補
        I_SHIFT = 1

        slope = features['spectrum'] - features['spectrum'].shift(I_SHIFT)
        is_falling = slope < 0

        can_trade = is_falling[1:] * (is_falling.shift(1)[1:] == False)
        windows = can_trade[can_trade].index
        periods = features.loc[windows, 'period']
        periods_half = [int(period) // 2 for period in periods]    

        # 候補を確保
        self.candidates['window'] = windows
        self.candidates['period_half'] = periods_half

        return periods_half

    def _calculate_offsets_candidate(self, periods_half):
        # 候補となる period それぞれに対し利益を最大にする offset を計算し、
        # その利益たちの中から最大のもの与える period, offset を求める。
        OFFSET_FIRST = 1

        fitnesses = []
        offsets = []

        for period_half in periods_half:
            period = period_half * 2

            fitnesses_at_the_offset = []
            for offset in range(OFFSET_FIRST, period + OFFSET_FIRST):
                params = {
                    'period_half': period_half,
                    'offset': offset
                }
                
                # パラメータを self.evaluate に直接渡せる形に適合させる。
                params = self._adapt_params_to_evaluate(params)

                fitness = self.evaluate(params)
                fitnesses_at_the_offset.append(fitness)

            # 最大適合度のインデックス
            ix = np.array(fitnesses_at_the_offset).argmax()

            # 最大適合度
            fitnesses.append(fitnesses_at_the_offset[ix])

            # 最大適合度を与える訓練オフセット
            offset = ix + OFFSET_FIRST
            offsets.append(offset)

        # 候補を確保
        self.candidates['offset'] = offsets

        return offsets, fitnesses
    
    def _select_the_best_ix(self, fitnesses):
        if len(fitnesses) == 0:
            return None

        ix = np.array(fitnesses).argmax()

        return ix
    
    @staticmethod
    def calculate_offset_test(period_half, offset_train, n_rows_train):
        period = period_half * 2

        # 最大適合度を与えるテストオフセット
        period_remaining = (n_rows_train - offset_train) % period

        if period_remaining < period_half:
            # long エントリー回数 == short エントリー回数 + 1
            # long エントリーが建玉になっている状態
            return period - period_remaining
        else:
            # long エントリー回数 == short エントリー回数
            # short エントリーが建玉になっている状態
            return period - period_remaining + period_half