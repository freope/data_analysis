from frestu.feature_selection import SelectorFeatureAbstract


class SelectorBlackColumns(SelectorFeatureAbstract):

    def __init__(self, ixs):
        """
        Parameters
        ----------
        ixs : list of int
            選択しないカラムのインデックスのリスト
        """
        self.__ixs = ixs
    
    def select(self, df):
        ixs = list(set(range(df.shape[1])) - set(self.__ixs))
        return df.iloc[:, ixs]