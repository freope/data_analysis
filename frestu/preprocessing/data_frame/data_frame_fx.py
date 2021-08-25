import pandas as pd
from frestu.preprocessing.data_frame import DataFrame


class DataFrameFx(DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def max_profit(self, col):
        diff = self.shift(-1) - self
        profit = diff[(diff > 0)[col]][col].sum()
        return profit
    
    def max_loss(self, col):
        diff = self.shift(-1) - self
        loss = diff[(diff < 0)[col]][col].sum()
        return loss