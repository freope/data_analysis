from frestu.feature_selection import SelectorFeatureAbstract


class SelectorWhiteColumns(SelectorFeatureAbstract):

    def __init__(self, ixs):
        """
        Parameters
        ----------
        ixs : list of int
            選択するカラムのインデックスのリスト
        """
        self.__ixs = ixs
    
    def select(self, df):
        return df.iloc[:, self.__ixs]