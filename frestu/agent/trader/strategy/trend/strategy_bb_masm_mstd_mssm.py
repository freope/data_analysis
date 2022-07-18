import pandas as pd

from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract
from frestu.feature_extraction.time_series import ExtractorMa
from frestu.feature_extraction.time_series import ExtractorMstd


class StrategyBbMasmMstdMssm(StrategyContinuousIndicatorAbstract):
    """
    Notes
    -----
    StrategyBb
        Masm(MaSlopeMa)
        Mstd
        Mssm(MstdSlopeMa)
    ポジション保有条件
        long
            移動平均の直近の平均的な傾きが正で、標準偏差が閾値より大きく、
            標準偏差の平均的な傾きが正
        short
            移動平均の直近の平均的な傾きが負で、標準偏差が閾値より大きく、
            標準偏差の平均的な傾きが正
    """

    def __init__(
            self, threshold, ma_type,
            window_bb, window_slope, window_slope_sigma):
        super().__init__()
        self.__threshold = threshold
        self.__extractor_ma = ExtractorMa(ma_type, window_bb)
        self.__extractor_mstd = ExtractorMstd(ma_type, window_bb)
        self.__window_slope = window_slope
        self.__window_slope_sigma = window_slope_sigma

    def calculate_open_indicators(self, df):
        ma = self.__extractor_ma.extract(df)
        sigma = self.__extractor_mstd.extract(df)

        # 移動平均の傾きの移動平均
        # slope = ma - ma.shift(1)
        # slope_ma = slope.rolling(self.__window_slope).mean()
        slope = ma - ma.shift(self.__window_slope)
        slope_ma = slope / self.__window_slope

        # 標準偏差の傾きの移動平均
        # slope_sigma = sigma - sigma.shift(1)
        # slope_sigma_ma = slope_sigma.rolling(self.__window_slope_sigma).mean()
        slope_sigma = sigma - sigma.shift(self.__window_slope_sigma)
        slope_sigma_ma = slope_sigma / self.__window_slope_sigma

        return slope_ma, sigma, slope_sigma_ma
    
    def convert_open_indicators(self, indicators, position_type):
        slope_ma, sigma, slope_sigma_ma = indicators

        if position_type == 'long':
            # 直近の平均的な傾きが正で、標準偏差が閾値より大きく、標準偏差の平均的な傾きが正。
            is_rising = pd.concat(
                [slope_ma > 0, sigma > self.__threshold, slope_sigma_ma > 0],
                axis=1).all(axis=1)
            return is_rising
        elif position_type == 'short':
            # 直近の平均的な傾きが負で、標準偏差が閾値より大きく、標準偏差の平均的な傾きが正。
            is_falling = pd.concat(
                [slope_ma < 0, sigma > self.__threshold, slope_sigma_ma > 0],
                axis=1).all(axis=1)
            return is_falling