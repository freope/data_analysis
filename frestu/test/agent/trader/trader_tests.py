import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader import Trader
from frestu.agent.trader.strategy.trend import StrategyGcdc


class TraderTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 0],
                ['2020-01-01 17:01:00', 10],
                ['2020-01-01 17:02:00', 20],
                ['2020-01-01 17:03:00', 30],
                ['2020-01-01 17:04:00', 25],
                ['2020-01-01 17:05:00', 15],
                ['2020-01-01 17:06:00', 5],
                ['2020-01-01 17:07:00', 10],
                ['2020-01-01 17:08:00', 30],
                ['2020-01-01 17:09:00', 60],
                ['2020-01-01 17:10:00', 70],
                ['2020-01-01 17:11:00', 10],
                ['2020-01-01 17:12:00', 20],
                ['2020-01-01 17:13:00', 30],
                ['2020-01-01 17:14:00', 25],
                ['2020-01-01 17:15:00', 15],
                ['2020-01-01 17:16:00', 5],
                ['2020-01-01 17:17:00', 10],
                ['2020-01-01 17:18:00', 30],
                ['2020-01-01 17:19:00', 60],
                ['2020-01-01 17:20:00', 70],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        self.trader = Trader()
        strategy = StrategyGcdc(2, 3)
        self.trader.trade(strategy, self.df)
        self.trader.abandon_the_oldest_position()
        self.trader.sum_up_positions()
        self.trader.sort_history()

    def tearDown(self):
        pass

    def test_open_positions(self):
        self.assertEqual(len(self.trader.open_positions), 1)

    def test_closed_positions(self):
        self.assertEqual(len(self.trader.closed_positions), 5)

    def test_correctly_closed_positions(self):
        self.assertEqual(len(self.trader.correctly_closed_positions), 5)

    def test_profits(self):
        profits = self.trader.profits
        # 利益なし
        self.assertEqual(profits.shape[0], 0)

    def test_losses(self):
        losses = self.trader.losses
        # 損失あり
        self.assertEqual(losses.iloc[0, 0], 15)
        self.assertEqual(losses.iloc[1, 0], 20)
    
    def test_cumulative_profits(self):
        cumulative_profits = self.trader.cumulative_profits
        self.assertEqual(cumulative_profits.iloc[0, 0], 0)
        self.assertEqual(cumulative_profits.iloc[1, 0], 0)

    def test_cumulative_losses(self):
        cumulative_losses = self.trader.cumulative_losses
        self.assertEqual(cumulative_losses.iloc[0, 0], 15)
        self.assertEqual(cumulative_losses.iloc[1, 0], 35)

    def test_total_net_profits(self):
        total_net_profits = self.trader.total_net_profits
        self.assertEqual(total_net_profits.iloc[0, 0], -15)

    def test_drawdowns(self):
        drawdowns = self.trader.drawdowns
        self.assertEqual(drawdowns.iloc[1, 0], 20)

    def test_total_net_profit(self):
        total_net_profit = self.trader.total_net_profit
        self.assertEqual(total_net_profit, -85)

    def test_gross_profit(self):
        gross_profit = self.trader.gross_profit
        self.assertEqual(gross_profit, 0)

    def test_gross_loss(self):
        gross_loss = self.trader.gross_loss
        self.assertEqual(gross_loss, 85)
    
    def test_profit_factor(self):
        profit_factor = self.trader.profit_factor
        self.assertEqual(profit_factor, 0)

    def test_maximal_drawdown(self):
        maximal_drawdown = self.trader.maximal_drawdown
        self.assertEqual(maximal_drawdown, 70)

    def test_total_trades_count(self):
        total_trades_count = self.trader.total_trades_count
        self.assertEqual(total_trades_count, 5)

    def test_long_positions_count(self):
        long_positions_count = self.trader.long_positions_count
        self.assertEqual(long_positions_count, 2)

    def test_short_positions_count(self):
        short_positions_count = self.trader.short_positions_count
        self.assertEqual(short_positions_count, 3)

    def test_long_win_rate(self):
        long_win_rate = self.trader.long_win_rate
        self.assertEqual(long_win_rate, 0)        

    def test_short_win_rate(self):
        short_win_rate = self.trader.short_win_rate
        self.assertEqual(short_win_rate, 0)

    def test_win_rate(self):
        win_rate = self.trader.win_rate
        self.assertEqual(win_rate, 0)

    def test_profit_trades_count(self):
        profit_trades_count = self.trader.profit_trades_count
        self.assertEqual(profit_trades_count, 0)

    def test_loss_trades_count(self):
        loss_trades_count = self.trader.loss_trades_count
        self.assertEqual(loss_trades_count, 5)
    
    def test_largest_profit(self):
        largest_profit = self.trader.largest_profit
        self.assertTrue(np.isnan(largest_profit))

    def test_largest_loss(self):
        largest_loss = self.trader.largest_loss
        self.assertEqual(largest_loss, 20)

    def test_average_profit(self):
        average_profit = self.trader.average_profit
        self.assertTrue(np.isnan(average_profit))

    def test_average_loss(self):
        average_loss = self.trader.average_loss
        self.assertEqual(average_loss, 17.0)

    def test_close_open_positions(self):
        self.assertEqual(len(self.trader.open_positions), 1)
        self.assertEqual(len(self.trader.closed_positions), 5)
        rate_last = self.df.iloc[-1, :]
        closing_time = rate_last.name
        closing_rate = rate_last[0]
        self.trader.close_open_positions(closing_time, closing_rate)
        self.assertEqual(len(self.trader.open_positions), 0)
        self.assertEqual(len(self.trader.closed_positions), 6)


if __name__ == '__main__':
    unittest.main()