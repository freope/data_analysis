import numpy as np

from frestu.feature_selection import SelectorFeatureAbstract


class SelectorEachColumn(SelectorFeatureAbstract):

    def __init__(self, zerones):
        """
        Parameters
        ----------
        zerones : list of int
            0 か 1 が df のカラム数だけ入ったリスト。
            0 は選択しない、1 は選択すると言う意味。
        """
        self.__zerones = zerones
    
    def select(self, df):
        ixs = np.where(np.array(self.__zerones) == 1)[0]
        return df.iloc[:, ixs]