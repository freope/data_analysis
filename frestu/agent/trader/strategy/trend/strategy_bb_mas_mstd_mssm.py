from frestu.agent.trader.strategy.trend import StrategyBbMasmMstdMssm


class StrategyBbMasMstdMssm(StrategyBbMasmMstdMssm):
    """
    Notes
    -----
    StrategyBb
        Mas(MaSlope)
        Mstd
        Mssm(MstdSlopeMa)
    ポジション保有条件
        long
            移動平均の直近の傾きが正で、標準偏差が閾値より大きく、標準偏差の平均的な傾きが正
        short
            移動平均の直近の傾きが負で、標準偏差が閾値より大きく、標準偏差の平均的な傾きが正
    """

    def __init__(self, threshold, ma_type, window_bb, window_slope_sigma):
        window_slope = 1
        super().__init__(
            threshold, ma_type, window_bb, window_slope, window_slope_sigma)