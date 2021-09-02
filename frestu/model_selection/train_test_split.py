import pandas as pd
from sklearn.model_selection import TimeSeriesSplit


def train_test_split_time_series(data_frame, n_splits):
    def _train_test_split_time_series():
        tscv = TimeSeriesSplit(n_splits=n_splits)
        for _, test_index in tscv.split(data_frame):
            ix_test = data_frame.iloc[test_index].index
            ix_train = pd.Index(sorted(set(data_frame.index) - set(ix_test)))
            yield ix_train, ix_test
    return _train_test_split_time_series