import os

import pandas as pd

from frestu.validation.ga import ValidatorGaAbstract


class Validator(ValidatorGaAbstract):

    def __init__(
            self,
            create_evaluating,
            chromosome_prototype,
            select,
            pop_size, n_eletes, gen_max, patience,
            create_evaluating_pred=None,
            async_evaluation='task',
            prefix_fitness='fitness_', prefix_chromosome='chromosome_'):
        super().__init__(
            chromosome_prototype,
            select,
            pop_size, n_eletes, gen_max, patience,
            async_evaluation,
            prefix_fitness, prefix_chromosome)
        self._create_evaluating = create_evaluating
        if create_evaluating_pred is None:
            self._create_evaluating_pred = create_evaluating
        else:
            self._create_evaluating_pred = create_evaluating_pred

    def fit(self, df, span_fitting, dpath):
        first = span_fitting[0]
        last = span_fitting[1]
        evaluate = self._create_evaluating(df.iloc[first:last, :])
        super().fit(evaluate, dpath)

    def predict(self, df, spans_pred, dpath):
        pred_spans_fitnesses = []
        for first, last in spans_pred:
            evaluate = self._create_evaluating_pred(
                df.iloc[first:last, :])
            fitnesses = [
                evaluate(ind.chromosome) for ind in self.population.individuals]
            pred_spans_fitnesses.append(fitnesses)

        # データフレーム化
        pred_spans_fitnesses = pd.DataFrame(pred_spans_fitnesses).T

        # 保存
        path = os.path.join(dpath, self._fname_fitness_pred())
        pred_spans_fitnesses.to_csv(path)

        return pred_spans_fitnesses

    def validate(self, df, span_fitting, spans_pred, dpath):
        self.fit(df, span_fitting, dpath)
        self.predict(df, spans_pred, dpath)