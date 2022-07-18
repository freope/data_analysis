from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorIdentity(ExtractorFeatureAbstract):

    def extract(self, df):
        return df