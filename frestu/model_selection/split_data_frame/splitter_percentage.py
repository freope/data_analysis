from frestu.model_selection.split_data_frame import SplitterDataFrameAbstract
from frestu.model_selection.split_data_frame import SplitterNumber


class SplitterPercentage(SplitterDataFrameAbstract):

    def __init__(
            self,
            percentage, y_col,
            can_dropna_train=True,
            can_dropna_test=False,
            can_dropna_test_x=True):
        """
        Parameters
        ----------
        y_col : int, str
            説明変数となるカラム番号またはカラム名
        """
        if not 0 <= percentage <= 1:
            raise ValueError('should be 0 <= percentage <= 1')

        self.__percentage = percentage
        self.__y_col = y_col
        self.__can_dropna_train = can_dropna_train
        self.__can_dropna_test = can_dropna_test
        self.__can_dropna_test_x = can_dropna_test_x
    
    def split(self, df):
        n_train = round(df.shape[0] * self.__percentage)
        splitter = SplitterNumber(
            n_train, self.__y_col,
            self.__can_dropna_train,
            self.__can_dropna_test,
            self.__can_dropna_test_x)
        return splitter.split(df)