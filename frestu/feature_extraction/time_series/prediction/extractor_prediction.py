import pandas as pd

from frestu.feature_extraction.extractor_feature_abstract import ExtractorFeatureAbstract


class ExtractorPrediction(ExtractorFeatureAbstract):
    """
    Attributes
    ----------
    X_train : pandas.core.frame.DataFrame
    y_train : pandas.core.frame.DataFrame
    X_test : pandas.core.frame.DataFrame
    y_test : pandas.core.frame.DataFrame
    y_pred_train : pandas.core.series.Series, numpy.ndarray
    y_pred_test : pandas.core.series.Series, numpy.ndarray
    y_pred : pandas.core.frame.DataFrame
    """

    def __init__(
            self,
            extractor, selector, splitter, predictor,
            can_fit=True, can_predict_train=False):
        self.extractor = extractor
        self.selector = selector
        self.splitter = splitter
        self.predictor = predictor
        self.__can_fit = can_fit
        self.__can_predict_train = can_predict_train
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.y_pred_train = None
        self.y_pred_test = None
        self.y_pred = None

    def extract(self, df):
        # 特徴抽出
        feature = self.extractor.extract(df)

        # 特徴選択
        feature = self.selector.select(feature)

        # 説明変数と目的変数、学習データと予測データに分ける
        self.X_train, y_train, \
        self.X_test, y_test = self.splitter.split(feature)

        # 学習
        if self.__can_fit:
            self.predictor.fit(self.X_train, y_train)

        # 予測
        self.y_pred_test = self.predictor.predict(self.X_test)
        # train の予測結果は、後に使わいまま無駄になるケースもあるので。
        if self.__can_predict_train:
            self.y_pred_train = self.predictor.predict(self.X_train)

        # データフレーム化
        # NOTE: predict の結果を 1 次元にするために y_train, y_test を1 次元にする。
        # その為 split で y は pandas.core.series.Series になっている。
        # train
        ix_train = self.X_train.index
        self.y_train = pd.DataFrame(y_train, index=ix_train)
        # test
        ix_test = self.X_test.index
        self.y_test = pd.DataFrame(y_test, index=ix_test)
        # pred
        ix_pred = df.index
        # NOTE: NaN で初期化される。
        self.y_pred = pd.DataFrame(index=ix_pred, columns=self.y_test.columns)
        # y_train, y_test が 1 次元であるため colums[0] とできる。
        self.y_pred.loc[ix_test, self.y_test.columns[0]] = self.y_pred_test

        return self.y_pred