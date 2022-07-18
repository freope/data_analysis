class SpanMaker:

    def __init__(
            self,
            start_point,
            n_spans_fitting, n_spans_pred,
            step_fitting, step_pred):
        self.__start_point = start_point
        self.__n_spans_fitting = n_spans_fitting
        self.__n_spans_pred = n_spans_pred
        self.__step_fitting = step_fitting
        self.__step_pred = step_pred

    def make_spans_fitting_variable_amount_of_training_data(self):
        spans_fitting = [
            [
                self.__start_point - self.__step_fitting * (i + 1),
                self.__start_point
            ]
            for i in range(self.__n_spans_fitting)
        ]
        return spans_fitting

    def make_spans_preds_variable_amount_of_training_data(self):
        spans_preds = [
            [
                [
                    self.__start_point + self.__step_pred * j,
                    self.__start_point + self.__step_pred * (j + 1)
                ]
                for j in range(self.__n_spans_pred)
            ]
            for _ in range(self.__n_spans_fitting)
        ]
        return spans_preds        

    def make_spans_fitting_variable_time_point(self, n_training_data):
        spans_fitting = [
            [
                self.__start_point + self.__step_fitting * i - n_training_data,
                self.__start_point + self.__step_fitting * i
            ]
            for i in range(self.__n_spans_fitting)
        ]
        return spans_fitting
    
    def make_spans_preds_variable_time_point(self):
        spans_preds = [
            [
                [
                    self.__start_point \
                        + self.__step_fitting * i + self.__step_pred * j,
                    self.__start_point \
                        + self.__step_fitting * i + self.__step_pred * (j + 1)
                ]
                for j in range(self.__n_spans_pred)
            ]
            for i in range(self.__n_spans_fitting)
        ]
        return spans_preds