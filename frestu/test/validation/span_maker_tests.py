import os
import sys
import unittest

sys.path.append(os.path.join('..'))
from frestu.validation import SpanMaker


class SpanMakerTests(unittest.TestCase):
    def setUp(self):
        self.start_point = 10
        self.n_spans_fitting = 20
        self.n_spans_pred = 30
        self.step_fitting = 2
        self.step_pred = 3
        self.span_maker = SpanMaker(
            self.start_point,
            self.n_spans_fitting, self.n_spans_pred,
            self.step_fitting, self.step_pred)

    def test_make_spans_variable_amount_of_training_data(self):
        spans_fitting = self.span_maker\
            .make_spans_fitting_variable_amount_of_training_data()
        spans_preds = self.span_maker\
            .make_spans_preds_variable_amount_of_training_data()

        # 個数の確認
        # fitting
        self.assertEqual(len(spans_fitting), self.n_spans_fitting)
        # pred
        self.assertEqual(len(spans_preds), self.n_spans_fitting)
        self.assertEqual(len(spans_preds[0]), self.n_spans_pred)

        # 値の確認
        # fitting
        self.assertEqual(
            spans_fitting[0][0], self.start_point - self.step_fitting)
        self.assertEqual(spans_fitting[0][1], self.start_point)
        self.assertEqual(
            spans_fitting[-1][0],
            self.start_point - self.step_fitting * self.n_spans_fitting)
        self.assertEqual(spans_fitting[-1][1], self.start_point)
        # pred 
        # 最初の学習に対する予測期間
        self.assertEqual(spans_preds[0][0][0], self.start_point)
        self.assertEqual(
            spans_preds[0][0][1], self.start_point + self.step_pred)
        self.assertEqual(
            spans_preds[0][-1][0],
            self.start_point + self.step_pred * (self.n_spans_pred - 1))
        self.assertEqual(
            spans_preds[0][-1][1],
            self.start_point + self.step_pred * self.n_spans_pred)
        # 最後の学習に対する予測期間
        self.assertEqual(spans_preds[-1][0][0], self.start_point)
        self.assertEqual(
            spans_preds[-1][0][1], self.start_point + self.step_pred)
        self.assertEqual(
            spans_preds[-1][-1][0],
            self.start_point + self.step_pred * (self.n_spans_pred - 1))
        self.assertEqual(
            spans_preds[-1][-1][1],
            self.start_point + self.step_pred * self.n_spans_pred)

    def test_make_spans_variable_time_point(self):
        n_training_data = 7
        spans_fitting = self.span_maker\
            .make_spans_fitting_variable_time_point(n_training_data)
        spans_preds = self.span_maker.make_spans_preds_variable_time_point()
        
        # 個数の確認
        # fitting
        self.assertEqual(len(spans_fitting), self.n_spans_fitting)
        # pred
        self.assertEqual(len(spans_preds), self.n_spans_fitting)
        self.assertEqual(len(spans_preds[0]), self.n_spans_pred)

        # 値の確認
        # fitting
        self.assertEqual(
            spans_fitting[0][0], self.start_point - n_training_data)
        self.assertEqual(spans_fitting[0][1], self.start_point)
        self.assertEqual(
            spans_fitting[-1][0],
            self.start_point - n_training_data \
                + (self.n_spans_fitting - 1) * self.step_fitting)
        self.assertEqual(
            spans_fitting[-1][1],
            self.start_point + (self.n_spans_fitting - 1) * self.step_fitting)
        # pred
        # 最初の学習に対する予測期間
        self.assertEqual(spans_preds[0][0][0], self.start_point)
        self.assertEqual(
            spans_preds[0][0][1], self.start_point + self.step_pred)
        self.assertEqual(
            spans_preds[0][-1][0],
            self.start_point + (self.n_spans_pred - 1) * self.step_pred)
        self.assertEqual(
            spans_preds[0][-1][1],
            self.start_point + self.n_spans_pred * self.step_pred)
        # 最後の学習に対する予測期間
        self.assertEqual(
            spans_preds[-1][0][0],
            self.start_point + (self.n_spans_fitting - 1) * self.step_fitting)
        self.assertEqual(
            spans_preds[-1][0][1],
            self.start_point \
                + (self.n_spans_fitting - 1) * self.step_fitting \
                + self.step_pred)
        self.assertEqual(
            spans_preds[-1][-1][0],
            self.start_point \
                + (self.n_spans_fitting - 1) * self.step_fitting \
                + (self.n_spans_pred - 1) * self.step_pred)
        self.assertEqual(
            spans_preds[-1][-1][1],
            self.start_point \
                + (self.n_spans_fitting - 1) * self.step_fitting \
                + self.n_spans_pred * self.step_pred)


if __name__ == '__main__':
    unittest.main()