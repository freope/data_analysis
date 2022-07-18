from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorMa


class ExtractorDfma(ExtractorFeatureAbstract):

    def __init__(self, ma_type, window):
        self.__extractor = ExtractorMa(ma_type, window)
    
    def extract(self, df):
        ma = self.__extractor.extract(df)
        return df - ma
