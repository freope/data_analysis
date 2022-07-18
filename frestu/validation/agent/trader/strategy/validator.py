import os

import pandas as pd

from frestu.validation import ValidatorAbstract


class Validator(ValidatorAbstract):
    
    def __init__(
            self,
            optimizer,
            create_evaluating,
            create_evaluating_fit=None,
            create_evaluating_pred=None,
            convert_params=lambda opt: opt.params,
            fname_params='strategy_parameters.txt',
            fname_fitness_fit='fitness_fit.txt',
            fname_fitness_pred='fitness_pred.txt'):
        self._optimizer = optimizer

        # 最適化用評価関数
        self._create_evaluating = create_evaluating

        # 訓練精度用評価関数
        if create_evaluating_fit is None:
            self._create_evaluating_fit = create_evaluating
        else:
            self._create_evaluating_fit = create_evaluating_fit

        # 予測精度用評価関数
        if create_evaluating_pred is None:
            self._create_evaluating_pred = create_evaluating
        else:
            self._create_evaluating_pred = create_evaluating_pred

        self._convert_params = convert_params
        self._fname_params = fname_params
        self._fname_fitness_fit = fname_fitness_fit
        self._fname_fitness_pred = fname_fitness_pred
    
    def fit(self, df, span_fitting, dpath):
        first = span_fitting[0]
        last = span_fitting[1]
        
        df_in_the_span = df.iloc[first:last, :]

        # 評価関数を生成
        evaluate = self._create_evaluating(df_in_the_span)

        # 最適化
        self._optimizer.evaluate = evaluate
        self._optimizer.optimize(df_in_the_span)

        # 適合度を計算
        evaluate = self._create_evaluating_fit(df_in_the_span)
        fitness = evaluate(self._optimizer.params)
        
        # 適合度を保存
        path = os.path.join(dpath, self._fname_fitness_fit)
        with open(path, 'wt') as file:
            file.write(str(fitness))
        
        # パラメータを保存
        # NOTE: params に numpy オブジェクト を含む場合、json.dumps() で文字列化して
        # 保存しようとするとシリアライズエラーが発生するので、Pandas を使って保存している。
        path = os.path.join(dpath, self._fname_params)
        pd.DataFrame(self._optimizer.params, index=[0]).T.to_csv(path)

    def predict(self, df, spans_pred, dpath):
        # 訓練用のパラメータからテスト用のパラメータを生成
        params_pred = self._make_params_pred()

        # 適合度を計算
        pred_spans_fitness = []
        for first, last in spans_pred:
            df_in_the_span = df.iloc[first:last, :]
            
            # 評価関数を生成
            evaluate = self._create_evaluating_pred(df_in_the_span)

            # 適合度を計算
            fitness = evaluate(params_pred)

            pred_spans_fitness.append(fitness)

        # データフレーム化
        pred_spans_fitness = pd.DataFrame(pred_spans_fitness).T

        # 保存
        path = os.path.join(dpath, self._fname_fitness_pred)
        pred_spans_fitness.to_csv(path)
        
    def validate(self, df, span_fitting, spans_pred, dpath):
        self.fit(df, span_fitting, dpath)
        self.predict(df, spans_pred, dpath)
    
    def _make_params_pred(self):
        """
        Notes
        -----
        self.optimizer 経由の値以外を使う場合、継承先のクラスでこのメソッドを上書きする。
        """
        return self._convert_params(self._optimizer)