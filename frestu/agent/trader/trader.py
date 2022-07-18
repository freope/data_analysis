import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from frestu.agent.trader import Position


class Trader:
    """
    Notes
    -----
    sort_history メソッドの実行を前提にしたメソッドがあることに注意。
    それらのメソッドは、先頭にその旨が記載されている。
    """

    def __init__(self, lot_size=1):
        # ロットの個数ではなく、1 ロット当たりの数量。2021 年現在 1000 が主流。
        self.__lot_size = lot_size
        self.__positions = []
        self.history = None
        # long
        self.__count_long = None
        self.__count_win_long = None
        # short
        self.__count_short = None
        self.__count_win_short = None
        self.__columns = [
            'opening_time', 'closing_time',
            'opening_rate', 'closing_rate',
            'position_type', 'position_size']
        self.__sort_column = 'opening_time'

    def trade(self, strategy, df):
        self.__positions = Position.create_positions(strategy, df)

    def calculate_positions_probability(self, probability_calculator, df=None):
        probability_calculator.set_positions_probability(self.__positions, df)

    def calculate_positions_size(self, position_size_calculator, df=None):
        position_size_calculator.set_positions_size(self.__positions, df)
    
    def abandon_the_oldest_position(self):
        """
        Notes
        -----
        - トレード開始時にエントリーしたポジションを破棄する。
        - ソートを利用しているので、その計算コストはかかる。そのコストが惜しい場合、
          コードの簡潔さを犠牲にして StrategyAbstract.create_positions() で、
          最も古いポジションを破棄する方法もあるが、コードの簡潔さを優先している。
        """
        positions = sorted(self.__positions, key=lambda p: p.opening_time)
        self.__positions = positions[1:]

    @property
    def positions(self):
        return self.__positions

    @property
    def open_positions(self):
        return list(filter(lambda pos: pos.is_open, self.__positions))

    @property
    def closed_positions(self):
        return list(filter(lambda pos: not(pos.is_open), self.__positions))

    @property
    def correctly_closed_positions(self):
        return list(filter(
            lambda pos: not(np.isnan(pos.closing_rate)),
            self.closed_positions))

    @property
    def correctly_closed_positions_with_valid_size(self):
        return list(filter(
            lambda pos: not(np.isnan(pos.position_size)),
            self.correctly_closed_positions))

    @property
    def profits(self):
        return self.history[self.__is_profit()].loc[:, ['profit']]

    @property
    def losses(self):
        return self.history[self.__is_loss()].loc[:, ['loss']]

    @property
    def cumulative_profits(self):
        # NOTE: ソート前提
        cumsum_profits = self.history.loc[:, ['profit']].cumsum()
        cumsum_profits.columns = ['cumulative_profit']
        return cumsum_profits
    
    @property
    def cumulative_losses(self):
        # NOTE: ソート前提
        cumsum_losses = self.history.loc[:, ['loss']].cumsum()
        cumsum_losses.columns = ['cumulative_loss']
        return cumsum_losses

    @property
    def total_net_profits(self):
        # NOTE: ソート前提
        cp = self.cumulative_profits['cumulative_profit']
        cl = self.cumulative_losses['cumulative_loss']
        total_net_profits = pd.DataFrame(cp - cl, columns=['total_net_profit'])
        return total_net_profits

    @property
    def drawdowns(self):
        # NOTE: ソート前提
        total_net_profits = self.total_net_profits
        drawdowns = []
        for ix in total_net_profits.index:
            previous_max = total_net_profits.iloc[:ix, 0].max()
            total_net_profit = total_net_profits.iloc[ix, 0]
            drawdown = previous_max - total_net_profit
            drawdowns.append(drawdown)
        drawdowns = pd.DataFrame(drawdowns, columns=['drawdown'])
        return drawdowns

    @property
    def total_net_profit(self):
        return self.gross_profit - self.gross_loss
    
    @property
    def gross_profit(self):
        return self.__profits().sum()
    
    @property
    def gross_loss(self):
        return self.__losses().sum()

    @property
    def profit_factor(self):
        if self.gross_loss == 0:
            return np.nan
        return self.gross_profit / self.gross_loss

    @property
    def expected_payoff(self):
        if self.total_trades_count == 0:
            return np.nan
        return self.total_net_profit / self.total_trades_count
    
    @property
    def maximal_drawdown(self):
        # NOTE: ソート前提
        return self.drawdowns['drawdown'].max()

    @property
    def total_trades_count(self):
        return self.__count_long + self.__count_short

    @property
    def long_positions_count(self):
        return self.__count_long

    @property
    def short_positions_count(self):
        return self.__count_short

    @property
    def long_win_rate(self):
        if self.__count_long == 0:
            return np.nan
        return self.__count_win_long / self.__count_long
    
    @property
    def short_win_rate(self):
        if self.__count_short == 0:
            return np.nan
        return self.__count_win_short / self.__count_short
    
    @property
    def win_rate(self):
        if self.total_trades_count == 0:
            return np.nan
        return  self.profit_trades_count / self.total_trades_count

    @property
    def profit_trades_count(self):
        return self.__count_win_long + self.__count_win_short
    
    @property
    def loss_trades_count(self):
        return self.total_trades_count - self.profit_trades_count
    
    @property
    def largest_profit(self):
        return self.__profits().max()
    
    @property
    def largest_loss(self):
        return self.__losses().max()
    
    @property
    def average_profit(self):
        return self.__profits().mean()
    
    @property
    def average_loss(self):
        return self.__losses().mean()
    
    @property
    def sort_column(self):
        return self.__sort_column

    def __profits(self):
        return self.profits['profit']
    
    def __losses(self):
        return self.losses['loss']

    def __is_profit(self):
        # history はソートし得るので、is_profit を属性でなくメソッド
        return self.history['profit'] > 0
    
    def __is_loss(self):
        # history はソートし得るので、is_loss を属性でなくメソッド
        return self.history['loss'] >= 0

    def __str__(self):
        return f'<Trader lot_size:{self.__lot_size}>'

    def summarize(self):
        attrs = {
            'total_net_profit': self.total_net_profit,
            'gross_profit': self.gross_profit,
            'gross_loss': self.gross_loss,
            'profit_factor': self.profit_factor,
            'expected_payoff': self.expected_payoff,
            'maximal_drawdown': self.maximal_drawdown,
            'total_trades_count': self.total_trades_count,
            'long_positions_count': self.long_positions_count,
            'short_positions_count': self.short_positions_count,
            'long_win_rate': self.long_win_rate,
            'short_win_rate': self.short_win_rate,
            'win_rate': self.win_rate,
            'profit_trades_count': self.profit_trades_count,
            'loss_trades_count': self.loss_trades_count,
            'largest_profit': self.largest_profit,
            'largest_loss': self.largest_loss,
            'average_profit': self.average_profit,
            'average_loss': self.average_loss}
        return json.dumps(attrs)

    def sum_up_positions(self):
        self.__create_history_from_positions()
        self.__create_profit_loss_columns()
        self.__calculate_count_long_count_win_long()
        self.__calculate_count_short_count_win_short()

    def __create_history_from_positions(self):
        closed_positions = self.correctly_closed_positions_with_valid_size

        positions = []
        for pos in closed_positions:
            position = [
                pos.opening_time, pos.closing_time,
                pos.opening_rate, pos.closing_rate,
                pos.position_type, pos.position_size]
            positions.append(position)

        self.history = pd.DataFrame(positions, columns=self.__columns)

    def __create_profit_loss_columns(self):
        # 一度も取引が発生しなかった場合
        if self.history.shape[0] == 0:
            self.history['profit'] = None
            self.history['loss'] = None
            return

        # 参照であることに注意
        df = self.history

        # 一時的な変数を保持するカラム
        # rate_difference
        df['rate_difference'] = df['closing_rate'] - df['opening_rate']
        # position_type_number
        df['position_type_number'] = 1
        is_short = df['position_type'] == 'short'
        df.loc[is_short, ['position_type_number']] = -1

        # profit
        df['profit'] = df['position_type_number'] \
            * df['rate_difference'] \
            * df['position_size'] \
            * self.__lot_size

        # 使うカラムを限定して上書き。rate_difference, position_type_number を削除
        columns = self.__columns + ['profit']
        self.history = self.history.loc[:, columns]

        # loss
        self.history['loss'] = self.history['profit'] * (-1)

        # profit, loss それぞれで、負の値を 0 にする
        self.history.loc[self.__is_loss(), 'profit'] = 0
        self.history.loc[self.__is_profit(), 'loss'] = 0

    def __calculate_count_long_count_win_long(self):
        # 一度も取引が発生しなかった場合
        if self.history.shape[0] == 0:
            self.__count_long = 0
            self.__count_win_long = 0
            return

        is_long = self.history['position_type'] == 'long'
        positions_long = self.history[is_long]
        self.__count_long = positions_long.shape[0]
        is_winning = positions_long['profit'] > 0
        self.__count_win_long = positions_long[is_winning].shape[0]
    
    def __calculate_count_short_count_win_short(self):
        # 一度も取引が発生しなかった場合
        if self.history.shape[0] == 0:
            self.__count_short = 0
            self.__count_win_short = 0
            return

        is_short = self.history['position_type'] == 'short'
        positions_short = self.history[is_short]
        self.__count_short = positions_short.shape[0]
        is_winning = positions_short['profit'] > 0
        self.__count_win_short = positions_short[is_winning].shape[0]

    def sort_history(self):
        self.history = self.history\
            .sort_values(self.__sort_column)\
            .reset_index(drop=True)
    
    def close_open_positions(self, closing_time, closing_rate):
        for open_position in self.open_positions:
            open_position.close(closing_time, closing_rate)

    @classmethod
    def visualize_trading(
            cls, trader, rate,
            title=None, path=None,
            freq='min', width_fig=16, height_fig=10):
        rate = rate.copy()
        rate.index = pd.to_datetime(rate.index)

        df = cls.calculate_trader_states(trader, freq)
        df = pd.concat([df, rate], axis=1)

        # concat したことによって生じ得る rate の欠損地を前の時点の値で補填
        df['rate'] = df['rate'].fillna(method='ffill')

        # 描画
        fig, ax1 = plt.subplots(figsize=(width_fig, height_fig))

        ax1.plot(df['rate'], label='Rate', color='C7')
        ax1.set_ylabel('Rate')
        ax1.legend(loc='upper left')
        
        ax2 = ax1.twinx()
        ax2.plot(df['profit'], label='Profit', color='C0')
        ax2.plot(df['loss'], label='Loss', color='C1')
        ax2.set_ylabel('Profit, loss')
        ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.96))

        # 先に描いて、グラフの優先順位を下げ、線が上書きされるようにする
        ax5 = ax1.twinx()
        ax5.plot(df['drawdown'], label='Drawdown', color='m')
        ax5.set_ylabel('Drawdown')
        ax5.legend(loc='upper left', bbox_to_anchor=(0, 0.78))
        ax5.spines['right'].set_position(('axes', 1.15))

        ax3 = ax1.twinx()
        ax3.plot(df['cumulative_profit'], label='Gross profit', color='b')
        ax3.plot(df['cumulative_loss'], label='Gross loss', color='r')
        ax3.set_ylabel('Gross profit, gross loss')
        ax3.legend(loc='upper left', bbox_to_anchor=(0, 0.89))
        ax3.spines['right'].set_position(('axes', 1.05))

        ax4 = ax1.twinx()
        ax4.plot(df['total_net_profit'], label='Total net profit', color='g')
        ax4.set_ylabel('Total net profit')
        ax4.legend(loc='upper left', bbox_to_anchor=(0, 0.82))
        ax4.spines['right'].set_position(('axes', 1.10))

        plt.grid()

        if title:
            plt.title(title)

        if path:
            plt.savefig(path)

    @staticmethod
    def calculate_trader_states(trader, freq='min'):
        """
        Notes
        -----
        インデックスに重複があると、profits.reindex(time_index) で
        ValueError: cannot reindex from a duplicate axis が発生するので、
        重複があり得る closing_time でなく、重複のない opening_time がインデックス。
        """
        # 累積和を計算するので history をソートしておく必要がある。
        trader.sort_history()

        df = pd.concat(
            [
                trader.profits,
                trader.losses,
                trader.cumulative_profits,
                trader.cumulative_losses,
                trader.total_net_profits,
                trader.drawdowns,
                pd.to_datetime(trader.history[trader.sort_column])
            ],
            axis=1)

        # インデックスを設定
        df = df.set_index('opening_time')

        # インデックスを時間的に連続にする
        index_column = trader.sort_column
        start = trader.history[index_column].head(1).values[0]
        end = trader.history[index_column].tail(1).values[0]
        time_index = pd.date_range(start=start, end=end, freq=freq)
        df = df.reindex(time_index)

        # 欠損値の補填
        # profit, loss は 0 で補填
        columns = ['profit', 'loss']
        df.loc[:, columns] = df.loc[:, columns].fillna(0)
        # その他は、前の時点の値で補填
        columns = [
            'cumulative_profit', 'cumulative_loss',
            'total_net_profit', 'drawdown']
        df.loc[:, columns] = df.loc[:, columns].fillna(method='ffill')

        return df