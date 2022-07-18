import pandas as pd

from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorOhlc


class ExtractorDmi(ExtractorFeatureAbstract):

    def __init__(self, window_ohlc, window_tr_dm, window_adx=None):
        self.__extractor_ohlc = ExtractorOhlc(window_ohlc)
        self.__window_tr_dm = window_tr_dm
        self.__window_adx = window_adx
    
    def extract(self, df):
        ohlc = self.__extractor_ohlc.extract(df)

        # TR
        tr1 = ohlc['high'] - ohlc['closing'].shift(1)
        tr2 = ohlc['closing'].shift(1) - ohlc['low']
        tr3 = ohlc['high'] - ohlc['low']
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # DM
        h_diff = ohlc['high'] - ohlc['high'].shift(1)
        l_diff = ohlc['low'].shift(1) - ohlc['low'] 
        p_dm = h_diff.copy()
        m_dm = l_diff.copy()
        p_dm[~(h_diff > l_diff)] = 0
        m_dm[~(h_diff < l_diff)] = 0

        # DI
        tr_rsum = tr.rolling(self.__window_tr_dm).sum()
        p_dm_rsum = p_dm.rolling(self.__window_tr_dm).sum()
        m_dm_rsum = m_dm.rolling(self.__window_tr_dm).sum()
        p_di = p_dm_rsum / tr_rsum
        m_di = m_dm_rsum / tr_rsum

        if not self.__window_adx:
            dmi = pd.concat([p_di, m_di], axis=1)
            dmi.columns = ['+DI', '-DI']
            return dmi

        # DX
        dx = (p_di - m_di).abs() / (p_di + m_di)

        # ADX
        adx = dx.rolling(self.__window_adx).mean()

        dmi = pd.concat([p_di, m_di, adx], axis=1)
        dmi.columns = ['+DI', '-DI', 'ADX']

        return dmi