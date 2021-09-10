import itertools

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
    
    def create_column_polynomial(
            self, columns, degrees, suffix='_poly_', inplace=False):
        """
        n 次式のカラムを作成する

        Parameters
        ----------
        column : str
            n 次式をとるカラム名
        degrees : list of number
            n の値のリスト。整数でない実数も指定可能。
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
        >>> df.create_column_polynomial('val', [0.5, 2, 3])
        """
        if inplace:
            df = self
        else:
            df = self.copy()

        poly_dfs = []
        columns_name = []
        for column, degree in itertools.product(columns, degrees):
            poly_dfs.append(df[column] ** degree)
            columns_name.append(column + suffix + str(degree))

        poly_dfs = pd.concat(poly_dfs, axis=1)
        poly_dfs.columns = columns_name

        df = pd.concat([df, poly_dfs], axis=1)

        return self.__class__(df)

    def create_column_log(self, columns, suffix='_log', inplace=False):
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
        >>> df.create_column_log('val')
        """
        if inplace:
            df = self
        else:
            df = self.copy()

        log_dfs = []
        columns_name = []
        for column in columns:
            log_dfs.append(pd.DataFrame(np.log(df[column])))
            columns_name.append(column + suffix)

        log_dfs = pd.concat(log_dfs, axis=1)
        log_dfs.columns = columns_name

        df = pd.concat([df, log_dfs], axis=1)

        return self.__class__(df)

    def create_columns_diff(
        self, columns, shifts, suffix='_diff_', inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        diff_dfs = []
        columns_name = []
        for column, i_shift in itertools.product(columns, shifts):
            diff_dfs.append(df[column] - df[column].shift(i_shift))
            columns_name.append(column + suffix + str(i_shift))

        diff_dfs = pd.concat(diff_dfs, axis=1)
        diff_dfs.columns = columns_name

        df = pd.concat([df, diff_dfs], axis=1)

        return self.__class__(df)

    def create_columns_past(
            self, columns, shifts, suffix='_past_', inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        shifted_dfs = []
        columns_name = []
        for column, i_shift in itertools.product(columns, shifts):
            shifted_dfs.append(df[column].shift(i_shift))
            columns_name.append(column + suffix + str(i_shift))

        shifted_dfs = pd.concat(shifted_dfs, axis=1)
        shifted_dfs.columns = columns_name

        df = pd.concat([df, shifted_dfs], axis=1)

        return self.__class__(df)
    
    def create_columns_future(
            self, columns, shifts, suffix='_future_', inplace=False):
        if inplace:
            df = self
        else:
            df = self.copy()

        shifted_dfs = []
        columns_name = []
        for column, i_shift in itertools.product(columns, shifts):
            shifted_dfs.append(df[column].shift(-i_shift))
            columns_name.append(column + suffix + str(i_shift))

        shifted_dfs = pd.concat(shifted_dfs, axis=1)
        shifted_dfs.columns = columns_name

        df = pd.concat([df, shifted_dfs], axis=1)

        return self.__class__(df)        