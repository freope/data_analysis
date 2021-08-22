import pandas as pd
from frestu.utils.string import new_string


class DataFrameFrestu(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(pd.DataFrame(*args, **kwargs))
    
    def make_index_unique(self, inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        cols = df.columns
        col_tmp = new_string(cols)
        df[col_tmp] = df.index

        # 重複を除く
        df.drop_duplicates(subset=[col_tmp], inplace=True)

        # カラムを元に戻す
        df = df[cols]
        
        return self.__class__(df)

    def complement_missing_minutes(self, inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        # インデックスが datetime 型になっている必要がある
        if type(df.index[0]) != pd._libs.tslibs.timestamps.Timestamp:
            df.index = pd.to_datetime(df.index)
        
        start = df.head(1).index[0]
        end = df.tail(1).index[0]
        time_index = pd.date_range(start=start, end=end, freq='min')

        # インデックスを更新し、欠損レコードを補間
        df = df.reindex(time_index)
        
        return self.__class__(df)

    def select_business_minutes(self, inplace=False):
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
        business_dates = pd.DataFrame(pd.date_range(start=start, end=end, freq='B'), columns=[col_right_on])

        # %M:%h:%s を除いた列を生成
        df[col_left_on] = df.index.strftime('%Y-%m-%d').astype(business_dates.dtypes[col_right_on])

        # インデックスを退避
        df[col_index] = df.index

        # 内部結合することで、営業日でない日のレコードを除く
        df = df.merge(business_dates, left_on=col_left_on, right_on=col_right_on)

        # 退避したインデックスを再設定（マージしたことでインデックスが失われるため）
        df.set_index(col_index, inplace=True)
        
        # カラムを元に戻す
        df = df[cols]
        
        # インデックス名を元に戻す（set_index で名前が変わっている）
        df.index.name = index_name        

        return self.__class__(df)