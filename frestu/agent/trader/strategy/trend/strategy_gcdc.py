from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyGcdc(StrategyDbma):
    """
    Golden Cross Dead Cross
    """

    def __init__(self, window_shorter, window_longer):
        """
        複数の移動平均を計算する為のパラメータを初期化

        Parameters
        ----------
        window_shorter: int
            移動平均の短い方の窓サイズ
        window_longer: int
            移動平均の長い方の窓サイズ

        Returns
        -------
        None
        """
        super().__init__('sma', window_shorter, 'sma', window_longer)