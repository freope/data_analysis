import copy

import pandas as pd

from frestu.model_selection import train_test_split_time_series
from frestu.optimization.ga.evaluation.evaluator_abstract import EvaluatorAbstract


class EvaluatorRegression(EvaluatorAbstract):

    def __init__(
            self,
            model_class,
            X, y,
            translate_chromosome,
            calculate_score,
            convert_scores_to_fitness,
            alternative_to_nan=-9999):
        super().__init__()
        self.model_class = model_class
        self.X = X
        self.y = y
        self.translate_chromosome = translate_chromosome
        self.calculate_score = calculate_score
        self.convert_scores_to_fitness = convert_scores_to_fitness
        self.alternative_to_nan = alternative_to_nan
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

    def create_evaluating_by_cross_validation(self, n_splits):
        def evaluate(chromosome):
            self.chromosome = chromosome
            # コピーしないと元の chromosome が破壊されるため
            chrom = copy.copy(chromosome)
            hparams, fparams = self.translate_chromosome(chrom)

            # 全ての特徴量が選択されなければ、alternative_to_nan を返す。
            if not(fparams.any()):
                return self.alternative_to_nan

            X_selected = self.X.loc[:, fparams]

            scores = []
            folds = train_test_split_time_series(X_selected, n_splits=n_splits)
            for ix_train, ix_test in folds():
                self.X_train = X_selected.loc[ix_train]
                self.X_test = X_selected.loc[ix_test]
                self.y_train = self.y.loc[ix_train]
                self.y_test = self.y.loc[ix_test]

                self.model = self.model_class(**hparams)
                self.model.fit(self.X_train, self.y_train.values.ravel())

                y_pred_train = self.model.predict(self.X_train)
                self.y_pred_train = pd.DataFrame(
                    y_pred_train, index=self.y_train.index)
                self.score_train = self.calculate_score(
                    self.y_train, self.y_pred_train)

                y_pred_test = self.model.predict(self.X_test)
                self.y_pred_test = pd.DataFrame(
                    y_pred_test, index=self.y_test.index)
                self.score_test = self.calculate_score(
                    self.y_test, self.y_pred_test)

                scores.append(self.score_test)

                self.notify_observers()

            fitness = self.convert_scores_to_fitness(scores)
            return fitness

        return evaluate