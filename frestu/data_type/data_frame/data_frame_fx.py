import pandas as pd

from frestu.data_type.data_frame import DataFrame
from frestu.util.string import new_string


class DataFrameFx(DataFrame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sum_rising(self, col):
        diff = self[col] - self.shift(1)[col]
        rising = diff[diff > 0].sum()
        return rising
    
    def sum_falling(self, col):
        diff = self[col] - self.shift(1)[col]
        falling = diff[diff < 0].sum()
        return falling

    def sum_changing(self, col):
        diff = self[col] - self.shift(1)[col]
        changing = abs(diff).dropna().sum()
        return changing

    def select_business_minutes(self, inplace=False):
        """
        分足データから営業日の時刻のみ取り出す

        Parameters
        ----------
        inplace : boolean, optional
            データフレームを置き換える。デフォルトは False。
        
        Returns
        -------
        self : DataFrame
            自身のデータフレーム

        Examples
        --------
        >>> df.select_business_minutes()
        """
        if inplace:
            df = self
        else:
            df = self.copy()

        index_name = df.index.name
        cols = df.columns
        col_right_on = 'business_date'
        col_left_on = new_string(cols)
        col_index = new_string(cols)

        start = df.head(1).index[0].strftime('%Y-%m-%d')
        end = df.tail(1).index[0].strftime('%Y-%m-%d')
        business_dates = pd.DataFrame(
            pd.date_range(start=start, end=end, freq='B'),
            columns=[col_right_on])

        # %M:%h:%s を除いた列を生成
        df[col_left_on] = df.index.strftime('%Y-%m-%d') \
            .astype(business_dates.dtypes[col_right_on])

        # インデックスを退避
        df[col_index] = df.index

        # 内部結合することで、営業日でない日のレコードを除く
        df = df.merge(business_dates,
                      left_on=col_left_on, right_on=col_right_on)

        # 退避したインデックスを再設定（マージしたことでインデックスが失われるため）
        df.set_index(col_index, inplace=True)
        
        # カラムを元に戻す
        df = df[cols]
        
        # インデックス名を元に戻す（set_index で名前が変わっている）
        df.index.name = index_name        

        return self.__class__(df)