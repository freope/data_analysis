from frestu.model_selection.split_data_frame import SplitterDataFrameAbstract


class SplitterIndex(SplitterDataFrameAbstract):

    def __init__(
            self,
            ix_train, ix_test, y_col,
            can_dropna_train=True,
            can_dropna_test=False,
            can_dropna_test_x=True):
        self.ix_train = ix_train
        self.ix_test = ix_test
        self.__y_col = y_col
        self.__can_dropna_train = can_dropna_train
        self.__can_dropna_test = can_dropna_test
        self.__can_dropna_test_x = can_dropna_test_x
    
    def split(self, df):
        df_train = df.loc[self.ix_train]
        df_test = df.loc[self.ix_test]

        if self.__can_dropna_train:
            df_train = df_train.dropna()
        
        if self.__can_dropna_test:
            df_test = df_test.dropna()

        if isinstance(self.__y_col, int):
            cols = df.columns
            # train
            X_train = df_train.drop(cols[self.__y_col], axis=1)
            y_train = df_train.iloc[:, self.__y_col]
            # test
            X_test = df_test.drop(cols[self.__y_col], axis=1)
            y_test = df_test.iloc[:, self.__y_col]
        elif isinstance(self.__y_col, str):
            # train
            X_train = df_train.drop(self.__y_col, axis=1)
            y_train = df_train[self.__y_col]
            # test
            X_test = df_test.drop(self.__y_col, axis=1)
            y_test = df_test[self.__y_col]
        else:
            raise ValueError('self.__y_col should be int or str.')
        
        if self.__can_dropna_test_x:
            X_test = X_test.dropna()

        return X_train, y_train, X_test, y_test