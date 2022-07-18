from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorDeviationRate(ExtractorFeatureAbstract):

    def __init__(self, window):
        self.__window = window
    
    def extract(self, df):
        ma = df.rolling(self.__window).mean()
        deviation_rate = (df - ma) / ma
        return deviation_rate