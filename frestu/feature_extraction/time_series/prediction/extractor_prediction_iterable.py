import numpy as np
import pandas as pd

from frestu.feature_extraction.extractor_feature_abstract import ExtractorFeatureAbstract


class ExtractorPredictionIterable(ExtractorFeatureAbstract):
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
            extractor, selector, splitter, splitter_test, predictor,
            builder, n_preds=1,
            df_external_pred=None, can_fillna=True,
            can_fit=True, can_predict_train=False):
        """
        Parameters
        ----------
        builder : a instance of BuilderAbstract
            引数に渡す builder は、build 実行した後のもの。
            extract メソッドの引数に渡す df を含む、より長い期間のデータで build を
            実行している。rebuild を実行する毎に、NaN を含む行が増える問題を回避するため。
        df_external_pred : pandas.core.frame.DataFrame
            builder.features と同じ期間。extract() の引数の df と同じ期間ではない。
        """
        self.extractor = extractor
        self.selector = selector
        self.splitter = splitter
        self.splitter_test = splitter_test
        self.predictor = predictor
        self.builder = builder
        self.__n_preds = n_preds
        self.df_external_pred = df_external_pred
        self.__can_fillna = can_fillna
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
        ix_df = df.index

        self.builder.reset_rebuilding()
        
        feature = self.builder.features

        # 特徴抽出
        feature = self.extractor.extract(feature)

        # 特徴選択
        feature = self.selector.select(feature)

        # 学習データと予測データに分ける
        # train
        self.X_train, y_train, \
        self.X_test, _ = self.splitter.split(feature.loc[ix_df])
        # test
        _, _, X_test, y_test = self.splitter_test.split(feature)

        # rebuild によりカラム名が更新されると predict を実行する際に、
        # FutureWarning: The feature names should match those that were passed
        # during fit. Starting version 1.2, an error will be raised.
        # が出るので、共有で使うカラム名を用意。
        cols_x = range(self.X_train.shape[1])

        # 学習
        if self.__can_fit:
            # 期間を限定
            self.X_train.columns = cols_x
            self.predictor.fit(self.X_train, y_train)

        # 予測
        X_test.columns = cols_x
        y_pred_test = self.predictor.predict(X_test)
        if self.__can_predict_train:
            # train は n_preds 回予測の結果ではないことに注意。
            self.X_train.columns = cols_x
            self.y_pred_train = self.predictor.predict(self.X_train)

        # データフレーム化
        # train
        ix_train = self.X_train.index
        self.y_train = pd.DataFrame(y_train, index=ix_train)
        # test
        ix_test = X_test.index
        y_test = pd.DataFrame(y_test, index=ix_test)
        # pred
        ix_pred = feature.index
        y_pred = pd.DataFrame(index=ix_pred, columns=y_test.columns)
        y_pred.loc[ix_test, y_test.columns[0]] = y_pred_test

        n_rebuildings = self.__n_preds - 1
        for _ in range(n_rebuildings):
            # rebuild
            if self.df_external_pred is None:
                self.builder.rebuild(y_pred)
            elif self.__can_fillna:
                # df_external_pred の期間を揃えて、欠損値 NaN を置換。
                future_shift = self.builder.future_shift
                df_external_pred = self.df_external_pred.shift(-future_shift)
                df_external_pred = df_external_pred.fillna(method='ffill')
                self.builder.rebuild(y_pred, df_external_pred)
            else:
                # df_external_pred の期間を揃える。
                future_shift = self.builder.future_shift
                df_external_pred = self.df_external_pred.shift(-future_shift)
                self.builder.rebuild(y_pred, df_external_pred)

            feature = self.builder.features

            # 特徴抽出
            feature = self.extractor.extract(feature)

            # 特徴選択
            feature = self.selector.select(feature)

            _, _, X_test, _ = self.splitter_test.split(feature)

            # 予測
            X_test.columns = cols_x
            y_pred_test = self.predictor.predict(X_test)

            # データフレーム化
            ix_test = X_test.index
            y_pred = pd.DataFrame(index=ix_pred, columns=y_test.columns)
            y_pred.loc[ix_test, y_test.columns[0]] = y_pred_test

        # df と同じ期間に限定
        self.y_pred = y_pred.loc[ix_df]
        # 訓練に使った期間に NaN を入れる
        self.y_pred.loc[ix_train] = np.nan

        # X_test と同じ期間に限定
        ix_test = self.X_test.index
        self.y_test = y_test.loc[ix_test]
        self.y_pred_test = self.y_pred.loc[ix_test].iloc[:, 0]

        return self.y_pred