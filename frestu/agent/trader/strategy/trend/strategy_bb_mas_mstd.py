from frestu.agent.trader.strategy.trend import StrategyBbMasmMstd


class StrategyBbMasMstd(StrategyBbMasmMstd):
    """
    Notes
    -----
    StrategyBb
        Mas(MaSlope)
        Mstd
    ポジション保有条件
        long
            移動平均の直近の傾きが正で、標準偏差が閾値より大きい
        short
            移動平均の直近の傾きが負で、標準偏差が閾値より大きい
    """

    def __init__(self, threshold, ma_type, window_bb):
        window_slope = 1
        super().__init__(threshold, ma_type, window_bb, window_slope)