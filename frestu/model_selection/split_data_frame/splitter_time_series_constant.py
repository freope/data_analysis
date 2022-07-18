import pandas as pd

from sklearn.model_selection import TimeSeriesSplit

from frestu.model_selection.split_data_frame import SplitterDataFrameAbstract


class SplitterTimeSeriesConstant(SplitterDataFrameAbstract):
    """
    Notes
    -----
    データ生成過程が不変の時系列データに対して使う。
    学習期間とテスト期間を分ければ、未来のデータも学習に使えるような時系列データ。
    """

    def __init__(self, df, n_splits):
        self.__df = df
        self.__n_splits = n_splits
    
    def split(self):
        tscv = TimeSeriesSplit(n_splits=self.__n_splits)

        for _, test_index in tscv.split(self.__df):
            ix_test = self.__df.iloc[test_index].index
            ix_train = pd.Index(sorted(set(self.__df.index) - set(ix_test)))
            yield ix_train, ix_test