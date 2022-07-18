import pandas as pd

from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorFuture(ExtractorFeatureAbstract):
    
    def __init__(self, future_shift, col_target, col_future='future'):
        """
        Parameters
        ----------
        col_target : int, str
            将来のカラムの元となる、カラム番号またはカラム名
        """
        if not 0 < future_shift:
            raise ValueError('should be 0 < future_shift.')
        self.__future_shift = future_shift
        self.__col_target = col_target
        self.__col_future = col_future
    
    def extract(self, df):
        """
        Notes
        -----
        df の時刻は昇順。下に行く程、新しいデータ。
        """

        if isinstance(self.__col_target, int):
            df_future = df.iloc[:, [self.__col_target]].shift(
                -self.__future_shift)
        elif isinstance(self.__col_target, str):
            df_future = df.loc[:, [self.__col_target]].shift(
                -self.__future_shift)
        else:
            raise ValueError('self.__col_target should be int or str.')

        df_future.columns = [self.__col_future]
        # 1 列目が予測対象
        return pd.concat([df_future, df], axis=1)