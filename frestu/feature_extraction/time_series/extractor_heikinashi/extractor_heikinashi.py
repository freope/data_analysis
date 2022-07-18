import pyximport
pyximport.install()

from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorOhlc
from frestu.feature_extraction.time_series.extractor_heikinashi.calculate_ha_open_with_cython import calculate_ha_open_with_cython


class ExtractorHeikinashi(ExtractorFeatureAbstract):

    def __init__(self, window, prefix='ha_', using_cython=True):
        self.__extractor_ohlc = ExtractorOhlc(window)
        self.__prefix = prefix
        self.__using_cython = using_cython

    def extract(self, df):
        prfx = self.__prefix
        ohlc = self.__extractor_ohlc.extract(df)

        # high
        ohlc[f'{prfx}high'] = ohlc['high']

        # low
        ohlc[f'{prfx}low'] = ohlc['low']

        # closing
        ohlc[f'{prfx}closing'] = ohlc.loc[
            :, ['open', 'high', 'low', 'closing']].mean(axis=1)

        # open
        self.__calculate_ha_open(ohlc, prfx)

        heikinashi = ohlc.loc[
            :, [f'{prfx}open',
                f'{prfx}high',
                f'{prfx}low',
                f'{prfx}closing']]

        return heikinashi
    
    def __calculate_ha_open(self, ohlc, prfx):
        if self.__using_cython:
            initial_ha_open = ohlc['open'][0]
            ha_closings = list(ohlc[f'{prfx}closing'])
            ha_opens = calculate_ha_open_with_cython(
                initial_ha_open, ha_closings)
            ohlc[f'{prfx}open'] = ha_opens
        else:
            ohlc[f'{prfx}open'] = ohlc['open']
            for ix, row in ohlc.iterrows():
                ohlc.loc[ix, f'{prfx}open'] = ohlc.shift(1).loc[
                    ix, [f'{prfx}open', f'{prfx}closing']].mean()