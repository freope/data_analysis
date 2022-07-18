from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorRsi(ExtractorFeatureAbstract):

    def __init__(self, window):
        self.__window = window
    
    def extract(self, df):
        df_diff = df - df.shift(1)

        is_rising = df_diff > 0
        is_falling = df_diff < 0

        rising = df_diff.copy()
        falling = -df_diff.copy()

        rising[is_falling] = 0
        falling[is_rising] = 0

        rising_rsum = rising.rolling(self.__window).sum()
        falling_rsum = falling.rolling(self.__window).sum()

        rsi = rising_rsum / (rising_rsum + falling_rsum)

        return rsi