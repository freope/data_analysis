from abc import abstractmethod, ABC


class StrategyAbstract(ABC):

    def __init__(self):
        """
        インディケータを計算するためのパラメータと、
        売買戦略のパラメータを属性として用意する。
        """
        self.frequency = 'min'
        self.time_format = '%Y-%m-%d %H:%M:%S'

    @abstractmethod
    def calculate_opening_times(self):
        """
        為替の時系列データを受け取り、OPEN 取引時刻と long/short を計算する。

        Parameters
        ----------
        df : DataFrame
            為替の時系列データ

        Returns
        -------
        (positions_long, positions_short) : taple of list
            positions_long や positions_short は、時刻のリスト。
        """
        pass

    @abstractmethod
    def calculate_closing_times(self):
        """
        ポジションに対応する、CLOSE 取引時刻を計算する。

        Parameters
        ----------
        df : DataFrame
            為替の時系列データ
        opening_times : list, optional
            時刻のリスト。

        Returns
        -------
        (closing_times_long, closing_times_short) : taple of list
            建玉を反対売買する時刻のリスト。まだない場合は None。
        """
        pass

    @abstractmethod
    def calculate_times(self):
        """
        Parameters
        ----------
        df : DataFrame
            為替の時系列データが入ったデータフレーム

        Returns
        -------
        (opening_times, closing_times) : tuple

        Notes
        -----
        - opening_times と closing_times の要素の順が対応している必要がある。
          建玉がある場合、
          1. 対応する closing_time の値を None にするか、
          2. opening_times の 末尾に建玉の opening_time が入っている
          必要がある。1, 2 を同時に使うこともできる。
          2 の場合、closing_times より opening_times の要素数が多いことになる。
        - opening_times と closing_times を別々に計算すると計算時間がかかる場合、
          これらを同時に計算する。
        """
        pass

    def create_positions(self, df):
        times = self.calculate_times(df)
        positions = self.__attach_position_type(times)
        positions = self.__attach_rate(df, positions)
        return positions

    def __attach_rate(self, df, positions):
        open_positions, closed_positions = positions

        # 建玉
        for pos in open_positions:
            pos['opening_rate'] = df.loc[pos['opening_time']].values[0]

        # エグジットしたポジション
        ixs = df.index
        for pos in closed_positions:
            pos['opening_rate'] = df.loc[pos['opening_time']].values[0]
                        
            # closing_time の行が欠損している場合もある。
            if pos['closing_time'] in ixs:
                pos['closing_rate'] = df.loc[pos['closing_time']].values[0]
            else:
                pos['closing_rate'] = np.nan
        
        return open_positions, closed_positions

    def __attach_position_type(self, times):
        """
        Notes
        -----
        positino_type, opening_time, closing_time を 1 つにまとめた辞書たちを作る。
        """
        opening_times, closing_times = times
        opening_times_long, opening_times_short = opening_times
        closing_times_long, closing_times_short = closing_times

        if len(opening_times_long) < len(closing_times_long):
            raise ValueError('the invalid number of times.')

        if len(opening_times_short) < len(closing_times_short):
            raise ValueError('the invalid number of times.')

        len_closing_times_long = len(closing_times_long)
        len_closing_times_short = len(closing_times_short)

        # long
        open_times_long = []
        closed_times_long = []
        
        # closing_time の値が（None の場合も含め）確定しているポジション
        for opening_time_long, closing_time_long in zip(
                opening_times_long[:len_closing_times_long],
                closing_times_long):

            attr = {
                'position_type': 'long',
                'opening_time': opening_time_long,
                'closing_time': closing_time_long,
            }

            # closing_time が None なら建玉に分類して次のループ
            if closing_time_long is None:
                open_times_long.append(attr)
                continue

            # opening_time < closing_time である必要
            if opening_time_long >= closing_time_long:
                raise ValueError('should be opening_time < closing_time.')

            closed_times_long.append(attr)

        # closing_time の値が確定していないポジション
        for opening_time_long in opening_times_long[len_closing_times_long:]:
            attr = {
                'position_type': 'long',
                'opening_time': opening_time_long,
                'closing_time': None,
            }
            open_times_long.append(attr)

        # short
        open_times_short = []
        closed_times_short = []

        # closing_time の値が（None の場合も含め）確定しているポジション
        for opening_time_short, closing_time_short in zip(
                opening_times_short[:len_closing_times_short],
                closing_times_short):

            attr = {
                'position_type': 'short',
                'opening_time': opening_time_short,
                'closing_time': closing_time_short,
            }

            # closing_time が None なら建玉に分類して次のループ
            if closing_time_short is None:
                open_times_short.append(attr)
                continue

            # opening_time < closing_time である必要
            if opening_time_short >= closing_time_short:
                raise ValueError('should be opening_time < closing_time.')

            closed_times_short.append(attr)

        # closing_time の値が確定していないポジション
        for opening_time_short in opening_times_short[len_closing_times_short:]:
            attr = {
                'position_type': 'short',
                'opening_time': opening_time_short,
                'closing_time': None,
            }
            open_times_short.append(attr)

        # long, short の情報を付与しているので足しても問題ない。
        open_times = open_times_long + open_times_short
        closed_times = closed_times_long + closed_times_short

        return open_times, closed_times

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)