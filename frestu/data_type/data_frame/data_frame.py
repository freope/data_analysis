import numpy as np
import pandas as pd

from frestu.util.string import new_string


class DataFrame(pd.DataFrame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(pd.DataFrame(*args, **kwargs))
    
    def make_index_unique(self, inplace=False):
        """
        重複しているインデックスを省く。

        Parameters
        ----------
        inplace : boolean, optional
            データフレームを置き換える。デフォルトは False。
        
        Returns
        -------
        self : DataFrame
            自身のデータフレーム

        Notes
        -----
        重複しているもののうち最初のものが残る。

        Examples
        --------
        >>> df.make_index_unique()
        """
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
        """
        欠損している時刻（分足）を NaN で補充する

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
        >>> df.complement_missing_minutes()
        """
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
        
    def create_column_log(self, column, suffix='_log', inplace=False):
        """
        自然対数を取ったカラムを作成する

        Parameters
        ----------
        column : str
            自然対数をとるカラム名
        suffix : str
            column で指定したカラム名の末尾に、この文字列を付加して、
            新たなカラムが作成される。
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

        log_df = pd.DataFrame(np.log(df[column]))
        log_df.columns = [column + suffix]

        df = pd.concat([df, log_df], axis=1)

        return self.__class__(df)

    def create_columns_diff(
        self, column, shifts, suffix='_diff_', inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        diff_dfs = [df[column] - df[column].shift(i) for i in shifts]
        columns_name = [column + suffix + str(i) for i in shifts]

        diff_dfs = pd.concat(diff_dfs, axis=1)
        diff_dfs.columns = columns_name

        df = pd.concat([df, diff_dfs], axis=1)

        return self.__class__(df)

    def create_columns_past(
            self, column, shifts, suffix='_past_', inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        shifted_dfs = [df[column].shift(i) for i in shifts]
        columns_name = [column + suffix + str(i) for i in shifts]

        shifted_dfs = pd.concat(shifted_dfs, axis=1)
        shifted_dfs.columns = columns_name

        df = pd.concat([df, shifted_dfs], axis=1)

        return self.__class__(df)
    
    def create_columns_future(
            self, column, shifts, suffix='_future_', inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        shifted_dfs = [df[column].shift(-i) for i in shifts]
        columns_name = [column + suffix + str(i) for i in shifts]

        shifted_dfs = pd.concat(shifted_dfs, axis=1)
        shifted_dfs.columns = columns_name

        df = pd.concat([df, shifted_dfs], axis=1)

        return self.__class__(df)        