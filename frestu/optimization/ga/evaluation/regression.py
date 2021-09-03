import copy

import pandas as pd

from frestu.model_selection import train_test_split_time_series


def create_evaluate_by_cross_validation(
        model_class,
        X, y,
        translate_chromosome,
        calculate_score,
        convert_scores_to_fitness,
        n_splits,
        monitor=lambda **kwargs: None,
        alternative_to_nan=-9999):
    def evaluate(chromosome):
        # コピーしないと元の chromosome が破壊されるため
        chrom = copy.copy(chromosome)
        hparams, fparams = translate_chromosome(chrom)

        # 全ての特徴量が選択されなければ、alternative_to_nan を返す。
        if not(fparams.any()):
            return alternative_to_nan

        X_selected = X.loc[:, fparams]

        scores = []
        folds = train_test_split_time_series(X_selected, n_splits=n_splits)
        for ix_train, ix_test in folds():
            X_train, X_test = X_selected.loc[ix_train], X_selected.loc[ix_test]
            y_train, y_test = y.loc[ix_train], y.loc[ix_test]

            model = model_class(**hparams)
            model.fit(X_train, y_train.values.ravel())

            y_train_pred = model.predict(X_train)
            y_train_pred = pd.DataFrame(y_train_pred, index=y_train.index)

            y_test_pred = model.predict(X_test)
            y_test_pred = pd.DataFrame(y_test_pred, index=y_test.index)

            score_test = calculate_score(y_test, y_test_pred)
            scores.append(score_test)

            monitor(
                chromosome=chromosome,
                model=model,
                score=score_test,
                X_train=X_train, X_test=X_test,
                y_train=y_train, y_test=y_test,
                y_train_pred=y_train_pred, y_test_pred=y_test_pred)

        fitness = convert_scores_to_fitness(scores)
        return fitness

    return evaluate