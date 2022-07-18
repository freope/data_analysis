import glob
import itertools
import json
import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from frestu.optimization.ga import Population
from frestu.optimization.ga import Individual
from frestu.validation import SpanMaker
from frestu.validation.ga import Validator


class ValidatorWfv(Validator):

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
            create_evaluating,
            chromosome_prototype,
            select,
            pop_size, n_eletes, gen_max, patience,
            create_evaluating_pred,
            async_evaluation,
            prefix_fitness, prefix_chromosome)
        self.preds_spans_fitnesses = []

    def predict(self, df, spans_pred, dpath):
        pred_spans_fitnesses = super().predict(df, spans_pred, dpath)
        self.preds_spans_fitnesses.append(pred_spans_fitnesses)

    def validate(self, df, spans_fitting, spans_preds, dpath):
        for span_fitting, spans_pred in zip(spans_fitting, spans_preds):
            dpath_child = os.path.join(
                dpath, self.__class__.dname_child(span_fitting))
            os.makedirs(dpath_child, exist_ok=True)
            self.fit(df, span_fitting, dpath_child)
            # self.population は、patience でストップした時のものであることに注意。
            self.predict(df, spans_pred, dpath_child)

    @classmethod
    def load_preds_spans_fitnesses(
            cls, dpath, fname_fitness_pred='fitness_pred.csv'):
        """
        Notes
        -----
        fitness_pred.csv が入っているディレクトリ名は、ソートにより古い順に
        並べられる名前になっている必要がある。
        """
        preds_spans_fitnesses = []

        paths = glob.glob(os.path.join(dpath, '*', fname_fitness_pred))
        paths = cls.sort_paths_fitness_pred(paths)

        for path in paths:
            pred_spans_fitnesses = pd.read_csv(path, index_col=0)
            preds_spans_fitnesses.append(pred_spans_fitnesses)
        return preds_spans_fitnesses

    @staticmethod
    def dname_child(span_fitting, sep='_'):
        """
        Notes
        -----
        ファイラで表示する際に、時刻が古い順になるように先頭を 0 で埋める。ファイラの場合、
        桁が違ってもこの方法で古い順に並ぶ。¥Python の sorted() で並び替えると、
        桁が異なる際に古い順にならないので、sort_paths_fitness_pred() を実装した。
        """
        width = max(len(str(span_fitting[0])), len(str(span_fitting[1])))
        fmt = '{0:>0' + str(width) + '}' + sep + '{1:>0' + str(width) + '}'
        return fmt.format(span_fitting[0], span_fitting[1])

    @staticmethod
    def sort_paths_fitness_pred(paths, sep='_'):
        paths = [pathlib.Path(path) for path in paths]
        paths = sorted(
            paths, key=lambda path: int(path.parent.name.partition(sep)[-1]))
        return paths

    @staticmethod
    def visualize_fitnesses(
            df, dpath,
            indices=None, columns_name=None,
            fname_fitnesses='fitnesses.png',
            fname_fitnesses_cumsum_rows='fitnesses_cumsum_rows.png',
            fname_fitnesses_cumsum_cols='fitnesses_cumsum_cols.png',
            width_fig=16, height_fig=10):    
        if indices:
            df.index = indices

        if columns_name:
            df.columns = columns_name

        plt.figure(figsize=(width_fig, height_fig))
        sns.heatmap(df, cmap='bwr', center=0)
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(dpath, fname_fitnesses))
        plt.close('all')

        plt.figure(figsize=(width_fig, height_fig))
        sns.heatmap(df.cumsum(axis=0), cmap='bwr', center=0)
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(dpath, fname_fitnesses_cumsum_rows))
        plt.close('all')

        plt.figure(figsize=(width_fig, height_fig))
        sns.heatmap(df.cumsum(axis=1), cmap='bwr', center=0)
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(dpath, fname_fitnesses_cumsum_cols))
        plt.close('all')

    @staticmethod
    def make_i_top_dataframe(preds_spans_fitnesses, i_top):
        df = pd.DataFrame([
            pred_spans_fitnesses.iloc[i_top, :]
            for pred_spans_fitnesses in preds_spans_fitnesses])
        return df
    
    @classmethod
    def visualize_validations_fitnesses(
            cls,
            dpath_validations,
            dpaths_validation,
            i_top=0,
            width_fig=16, 
            height_fig=10,
            fname_csv_sum_of_validations_fitnesses='sum_of_validations_fitnesses.csv',
            fname_csv_sum_of_validations_fitnesses_diff_event='sum_of_validations_fitnesses_diff_event.csv',
            fname_csv_std_of_validations_fitnesses='std_of_validations_fitnesses.csv',
            fname_csv_std_of_validations_fitnesses_diff_event='std_of_validations_fitnesses.csv',
            skip_visualizing_validations=False,
            fname_sum_of_validations_fitnesses='sum_of_validations_fitnesses.png',
            fname_sum_of_validations_fitnesses_gnuplot='sum_of_validations_fitnesses_gnuplot.png',
            fname_sum_of_validations_fitnesses_diff_event='sum_of_validations_fitnesses_diff_event.png',
            fname_sum_of_validations_fitnesses_diff_event_gnuplot='sum_of_validations_fitnesses_diff_event_gnuplot.png',
            fname_std_of_validations_fitnesses='std_of_validations_fitnesses.png',
            fname_std_of_validations_fitnesses_diff_event='std_of_validations_fitnesses_diff_event.png',
            skip_visualizing_each_validation=False,
            fname_fitnesses_diff_events='fitnesses_diff_events.png',
            fname_sum_of_fitnesses='sum_of_fitnesses.png',
            fname_sum_of_fitnesses_diff_events='sum_of_fitnesses_diff_events.png',
            fname_std_of_fitnesses='std_of_fitnesses.png',
            fname_std_of_fitnesses_diff_events='std_of_fitnesses_diff_events.png'):
        figsize = (width_fig, height_fig)

        sum_fitnesses = []
        std_fitnesses = []
        sum_fitnesses_diff_event = []
        std_fitnesses_diff_event = []

        for i_time, dpath_validation in enumerate(dpaths_validation):

            # 学習と予測の結果を読み込み
            preds_spans_fitnesses = cls.load_preds_spans_fitnesses(
                dpath_validation)

            # 最良個体の適合度で作成
            df_fitnesses = cls.make_i_top_dataframe(
                preds_spans_fitnesses, i_top)

            # イベントの影響を省く（平均を引く）
            fitnesses_simultaneous = [
                [] for _ in range(
                    df_fitnesses.shape[0] + df_fitnesses.shape[1] - 1)]

            for i, j in itertools.product(
                    range(df_fitnesses.shape[0]), range(df_fitnesses.shape[1])):
                fitnesses_simultaneous[i + j].append(df_fitnesses.iloc[i, j])

            events = []
            for fitnesses in fitnesses_simultaneous:
                events.append(sum(fitnesses) / len(fitnesses))

            df_fitnesses_diff_event = pd.DataFrame(np.zeros(df_fitnesses.shape))
            for i, j in itertools.product(
                    range(df_fitnesses.shape[0]), range(df_fitnesses.shape[1])):
                df_fitnesses_diff_event.iloc[i, j] \
                    = df_fitnesses.iloc[i, j] - events[i + j]

            sum_fitnesses.append(df_fitnesses.sum(axis=0))
            std_fitnesses.append(df_fitnesses.std(axis=0))
            sum_fitnesses_diff_event.append(df_fitnesses_diff_event.sum(axis=0))
            std_fitnesses_diff_event.append(df_fitnesses_diff_event.std(axis=0))

            if skip_visualizing_each_validation:
                continue

            # 描画
            range_xticks = range(df_fitnesses.shape[1])

            plt.figure(figsize=figsize)
            sns.heatmap(df_fitnesses_diff_event, cmap='bwr', center=0)
            plt.xlabel('Prediction')
            plt.ylabel('Fitting')
            plt.savefig(os.path.join(
                dpath_validation, fname_fitnesses_diff_events))
            plt.close('all')

            plt.figure(figsize=figsize)
            plt.plot(df_fitnesses.sum(axis=0))
            plt.xticks(range_xticks)
            plt.xlabel('Prediction')
            plt.ylabel('Fitness')
            plt.grid()
            plt.savefig(os.path.join(dpath_validation, fname_sum_of_fitnesses))
            plt.close('all')

            plt.figure(figsize=figsize)
            plt.plot(df_fitnesses_diff_event.sum(axis=0))
            plt.xticks(range_xticks)
            plt.xlabel('Prediction')
            plt.ylabel('Fitness')
            plt.grid()
            plt.savefig(os.path.join(
                dpath_validation, fname_sum_of_fitnesses_diff_events))
            plt.close('all')

            plt.figure(figsize=figsize)
            plt.plot(df_fitnesses.std(axis=0))
            plt.xticks(range_xticks)
            plt.xlabel('Prediction')
            plt.ylabel('Standard Deviation of Fitness')
            plt.grid()
            plt.savefig(os.path.join(dpath_validation, fname_std_of_fitnesses))
            plt.close('all')

            plt.figure(figsize=figsize)
            plt.plot(df_fitnesses_diff_event.std(axis=0))
            plt.xticks(range_xticks)
            plt.xlabel('Prediction')
            plt.ylabel('Standard Deviation of Fitness')
            plt.grid()
            plt.savefig(os.path.join(
                dpath_validation, fname_std_of_fitnesses_diff_events))
            plt.close('all')

        # CSV として保存
        pd.DataFrame(sum_fitnesses).to_csv(os.path.join(
            dpath_validations, fname_csv_sum_of_validations_fitnesses))
        pd.DataFrame(sum_fitnesses_diff_event).to_csv(os.path.join(
            dpath_validations,
            fname_csv_sum_of_validations_fitnesses_diff_event))
        pd.DataFrame(std_fitnesses).to_csv(os.path.join(
            dpath_validations, fname_csv_std_of_validations_fitnesses))
        pd.DataFrame(std_fitnesses_diff_event).to_csv(os.path.join(
            dpath_validations,
            fname_csv_std_of_validations_fitnesses_diff_event))

        if skip_visualizing_validations:
            return

        # 描画
        plt.figure(figsize=figsize)
        sns.heatmap(sum_fitnesses, cmap='bwr', center=0)
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(
            dpath_validations, fname_sum_of_validations_fitnesses))
        plt.close('all')

        plt.figure(figsize=figsize)
        sns.heatmap(sum_fitnesses, cmap='gnuplot')
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(
            dpath_validations, fname_sum_of_validations_fitnesses_gnuplot))
        plt.close('all')

        plt.figure(figsize=figsize)
        sns.heatmap(sum_fitnesses_diff_event, cmap='bwr', center=0)
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(
            dpath_validations, fname_sum_of_validations_fitnesses_diff_event))
        plt.close('all')

        plt.figure(figsize=figsize)
        sns.heatmap(sum_fitnesses_diff_event, cmap='gnuplot')
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(
            dpath_validations,
            fname_sum_of_validations_fitnesses_diff_event_gnuplot))
        plt.close('all')

        plt.figure(figsize=figsize)
        sns.heatmap(std_fitnesses, cmap='gnuplot')
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(
            dpath_validations, fname_std_of_validations_fitnesses))
        plt.close('all')

        plt.figure(figsize=figsize)
        sns.heatmap(std_fitnesses_diff_event, cmap='gnuplot')
        plt.xlabel('Prediction')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(
            dpath_validations, fname_std_of_validations_fitnesses_diff_event))
        plt.close('all')

    @classmethod
    def visualize_optimal_update_time_inverval(
            cls,
            dpath_validations,
            dpaths_validation,
            update_time_intervals,
            n_spans_pred,
            i_top=0,
            start_offset=0,
            width_fig=16,
            height_fig=10,
            fname_csv_update_time_interval='update_time_interval.csv',
            skip_visualizing_update_time_interval=False,
            fname_update_time_interval='update_time_interval.png',
            skip_visualizing_updated_profit_and_loss=False,
            fname_updated_profit_and_loss='updated_profit_and_loss_{}.png'):
        figsize = (width_fig, height_fig)
        
        sum_fitnesses_update_time_intervals = []

        for update_time_interval in update_time_intervals:

            fitnesses_update_time_intervals = []

            for i_time, dpath_validation in enumerate(dpaths_validation):

                # 学習と予測の結果を読み込み
                preds_spans_fitnesses = cls.load_preds_spans_fitnesses(
                    dpath_validation)

                fitnesses_update_time_interval = []

                # パラメータの更新頻度 update_time_interval で集計
                for i_term in range(0, n_spans_pred, update_time_interval):
                    ix_term = i_term + start_offset

                    # オフセットによっては preds が存在しなくなるため
                    if n_spans_pred <= ix_term:
                        continue

                    pred_span_fitnesses = preds_spans_fitnesses[ix_term]
                    fitnesses = \
                        pred_span_fitnesses.iloc[i_top, 0:update_time_interval]

                    for fitness in fitnesses:
                        fitnesses_update_time_interval.append(fitness)

                fitnesses_update_time_intervals.append(
                    fitnesses_update_time_interval)

            fitnesses_update_time_intervals = pd.DataFrame(
                fitnesses_update_time_intervals).iloc[:, :n_spans_pred]

            sum_fitnesses_update_time_intervals.append(
                fitnesses_update_time_intervals.sum(axis=1))

            if skip_visualizing_updated_profit_and_loss:
                continue

            # パラメータを更新頻度 update_time_interval で更新した際の日々の損益を描画
            plt.figure(figsize=figsize)
            sns.heatmap(fitnesses_update_time_intervals, cmap='bwr', center=0)
            plt.xlabel('Prediction')
            plt.ylabel('Fitting')
            plt.savefig(os.path.join(
                dpath_validations,
                fname_updated_profit_and_loss.format(update_time_interval)))
            plt.close('all')

        sum_fitnesses_update_time_intervals = \
            pd.DataFrame(sum_fitnesses_update_time_intervals).T

        # csv として保存
        sum_fitnesses_update_time_intervals.to_csv(os.path.join(
            dpath_validations, fname_csv_update_time_interval))

        if skip_visualizing_update_time_interval:
            return
        
        # 描画
        plt.figure(figsize=figsize)
        sns.heatmap(sum_fitnesses_update_time_intervals, cmap='bwr', center=0)
        plt.xlabel('Update Time Interval')
        plt.ylabel('Fitting')
        plt.savefig(os.path.join(dpath_validations, fname_update_time_interval))
        plt.close('all')