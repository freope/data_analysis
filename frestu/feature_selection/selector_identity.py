from frestu.feature_selection import SelectorFeatureAbstract


class SelectorIdentity(SelectorFeatureAbstract):

    def select(self, df):
        return df