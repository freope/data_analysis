import numpy as np

from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorMakingPastsNan(ExtractorFeatureAbstract):

    def __init__(self, extractor, n_pasts):
        self.__extractor = extractor
        self.__n_pasts = n_pasts
    
    def extract(self, df):
        """
        Notes
        -----
        df の時刻は昇順。下に行く程、新しいデータ。
        """
        feature = self.__extractor.extract(df)
        feature.iloc[0:self.__n_pasts] = np.nan
        return feature