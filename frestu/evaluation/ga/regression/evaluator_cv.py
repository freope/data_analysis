import copy

import pandas as pd

from frestu.evaluation import EvaluatorAbstract
from frestu.model_selection.split_data_frame import SplitterTimeSeriesConstant


class EvaluatorCv(EvaluatorAbstract):

    def __init__(
            self,
            model_class,
            translate_chromosome,
            calculate_score,
            convert_scores_to_fitness,
            n_splits):
        super().__init__()
        self.__model_class = model_class
        self.__translate_chromosome = translate_chromosome
        self.__calculate_score = calculate_score
        self.__convert_scores_to_fitness = convert_scores_to_fitness
        self.__n_splits = n_splits
        # Observer で参照するための変数
        # 遺伝子間で共有するので、並列評価では、正確な値を算出できないので注意。
        self.chromosome = None
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred_train = None
        self.y_pred_test = None
        self.score_train = None
        self.score_test = None
        self.fitness = None

    def create_evaluating(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため。
            chrom = copy.copy(chromosome)

            # model を交差検証の中で繰り返し初期化するので translate_chromosome は、
            # モデルを返さずにモデルのクラスを返している。
            params_model, \
            convert_data_to_xy = self.__translate_chromosome(chrom)

            # NOTE:
            # - 特徴抽出
            # - 特徴選択
            # - 説明変数と目的変数に分ける
            # の処理は data が与えられた後にしか実行できないため、
            # translate_chromosome の外で実行する必要がある。
            X, y = convert_data_to_xy(data)

            scores = []
            tscv = SplitterTimeSeriesConstant(X, self.__n_splits).split()
            for ix_train, ix_test in tscv:
                self.X_train = X.loc[ix_train]
                self.X_test = X.loc[ix_test]
                self.y_train = y.loc[ix_train]
                self.y_test = y.loc[ix_test]

                self.model = self.__model_class(**params_model)
                self.model.fit(self.X_train, self.y_train.values.ravel())

                y_pred_train = self.model.predict(self.X_train)
                self.y_pred_train = pd.DataFrame(
                    y_pred_train, index=self.y_train.index)
                self.score_train = self.__calculate_score(
                    self.y_train, self.y_pred_train)

                y_pred_test = self.model.predict(self.X_test)
                self.y_pred_test = pd.DataFrame(
                    y_pred_test, index=self.y_test.index)
                self.score_test = self.__calculate_score(
                    self.y_test, self.y_pred_test)

                scores.append(self.score_test)

                self.notify_observers()

            self.fitness = self.__convert_scores_to_fitness(scores)    
                    
            return self.fitness

        return evaluate
    
    def create_evaluating_by_extractor_prediction(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため。
            chrom = copy.copy(chromosome)

            # NOTE:
            # extractor_pred は、
            # - extractor
            # - selector
            # - splitter
            # は translate_chromosome の中でセットされている必要がある。
            # - predictor
            # は、交差検証ループの中でセットする。
            params_model, \
            extractor_pred = self.__translate_chromosome(chrom)

            scores = []
            tscv = SplitterTimeSeriesConstant(data, self.__n_splits).split()
            for ix_train, ix_test in tscv:
                # 説明変数と目的変数、学習データと予測データに分ける splitter を設定
                extractor_pred.splitter.ix_train = ix_train
                extractor_pred.splitter.ix_test = ix_test

                # 予測器を設定
                self.model = self.__model_class(**params_model)
                extractor_pred.predictor = self.model

                # 予測
                extractor_pred.extract(data)

                self.X_train = extractor_pred.X_train
                self.X_test = extractor_pred.X_test
                self.y_train = extractor_pred.y_train
                self.y_test = extractor_pred.y_test

                y_pred_train = extractor_pred.y_pred_train
                self.y_pred_train = pd.DataFrame(
                    y_pred_train, index=self.y_train.index)
                self.score_train = self.__calculate_score(
                    self.y_train, self.y_pred_train)

                y_pred_test = extractor_pred.y_pred_test
                self.y_pred_test = pd.DataFrame(
                    y_pred_test, index=self.y_test.index)
                self.score_test = self.__calculate_score(
                    self.y_test, self.y_pred_test)

                scores.append(self.score_test)

                self.notify_observers()

            self.fitness = self.__convert_scores_to_fitness(scores)    

            return self.fitness

        return evaluate