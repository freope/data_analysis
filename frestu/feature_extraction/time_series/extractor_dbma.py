from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorMa


class ExtractorDbma(ExtractorFeatureAbstract):

    def __init__(
            self,
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer):
        if not window_shorter < window_longer:
            raise ValueError('should be window_shorter < window_longer.')
        self.__extractor_shorter = ExtractorMa(ma_type_shorter, window_shorter)
        self.__extractor_longer = ExtractorMa(ma_type_longer, window_longer)

    def extract(self, df):
        ma_shorter = self.__extractor_shorter.extract(df)
        ma_longer = self.__extractor_longer.extract(df)
        return ma_shorter - ma_longer