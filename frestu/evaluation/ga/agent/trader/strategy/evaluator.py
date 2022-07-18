import copy
from statistics import stdev

from frestu.agent.trader import Trader
from frestu.evaluation import EvaluatorAbstract


class Evaluator(EvaluatorAbstract):

    def __init__(
            self,
            translate_chromosome,
            calculate_fitness,
            lot_size=1,
            can_abandon_the_oldest_position=False,
            can_end_with_open_positions=False,
            averaging_weights=None,
            rd_coeff=0):
        super().__init__()
        self.__translate_chromosome = translate_chromosome
        self.__calculate_fitness = calculate_fitness
        self.__lot_size = lot_size
        self.__can_abandon_the_oldest_position = can_abandon_the_oldest_position
        self.__can_end_with_open_positions = can_end_with_open_positions
        # on_averages
        self.__averaging_weights = averaging_weights
        # regularizing_deviation_coefficient
        self.__rd_coeff = rd_coeff
        # Observer で参照するための変数
        # 遺伝子間で共有するので、並列計算では、正確な値を算出できないので注意。
        self.chromosome = None
        self.trader = None
        self.fitness = None

    def create_evaluating(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため。
            chrom = copy.copy(chromosome)

            # 翻訳
            strategy = self.__translate_chromosome(chrom)

            self.trader = Trader(self.__lot_size)

            # トレード
            self.trader.trade(strategy, data)

            # 最も古いポジションを破棄
            if self.__can_abandon_the_oldest_position:
                self.trader.abandon_the_oldest_position()

            # 建玉をクローズ
            if not self.__can_end_with_open_positions:
                rate_last = data.iloc[-1, :]
                closing_time = rate_last.name
                closing_rate = rate_last[0]
                self.trader.close_open_positions(closing_time, closing_rate)

            # 集計
            self.trader.sum_up_positions()

            self.fitness = self.__calculate_fitness(self.trader)

            self.notify_observers()

            return self.fitness

        return evaluate

    def create_evaluating_on_average(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため
            chrom = copy.copy(chromosome)

            # 翻訳
            strategy = self.__translate_chromosome(chrom)

            n_data = data.shape[0]
            n_averages = len(self.__averaging_weights)
            n_data_in_segment = n_data // n_averages

            fitnesses_splitted = []
            self.fitness = 0
            for i_avg, weight in enumerate(self.__averaging_weights):
                first = n_data_in_segment * i_avg
                last = first + n_data_in_segment
                data_in_segment = data.iloc[first:last, :]

                self.trader = Trader(self.__lot_size)

                # トレード
                self.trader.trade(strategy, data_in_segment)

                # 最も古いポジションを破棄
                if self.__can_abandon_the_oldest_position:
                    self.trader.abandon_the_oldest_position()

                # 建玉をクローズ
                if not self.__can_end_with_open_positions:
                    rate_last = data.iloc[-1, :]
                    closing_time = rate_last.name
                    closing_rate = rate_last[0]
                    self.trader.close_open_positions(closing_time, closing_rate)

                # 集計
                self.trader.sum_up_positions()

                fitness = self.__calculate_fitness(self.trader)
                fitnesses_splitted.append(fitness)
                self.fitness += fitness * weight

            self.fitness -= self.__rd_coeff * stdev(fitnesses_splitted)

            self.notify_observers()

            return self.fitness

        return evaluate

    def create_evaluating_with_positions_size(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため
            chrom = copy.copy(chromosome)

            # 翻訳
            strategy, \
            probability_calculator, \
            position_size_calculator = self.__translate_chromosome(chrom)

            self.trader = Trader(self.__lot_size)

            # トレード
            self.trader.trade(strategy, data)

            # 最も古いポジションを破棄
            if self.__can_abandon_the_oldest_position:
                self.trader.abandon_the_oldest_position()

            # 建玉をクローズ
            if not self.__can_end_with_open_positions:
                rate_last = data.iloc[-1, :]
                closing_time = rate_last.name
                closing_rate = rate_last[0]
                self.trader.close_open_positions(closing_time, closing_rate)

            # 確率の計算
            self.trader.calculate_positions_probability(
                probability_calculator, data)

            # レバレッジの計算
            self.trader.calculate_positions_size(position_size_calculator, data)

            # 集計
            self.trader.sum_up_positions()

            self.fitness = self.__calculate_fitness(self.trader)

            self.notify_observers()

            return self.fitness

        return evaluate

    def create_evaluating_with_positions_size_on_average(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため
            chrom = copy.copy(chromosome)

            # 翻訳
            strategy, \
            probability_calculator, \
            position_size_calculator = self.__translate_chromosome(chrom)

            n_data = data.shape[0]
            n_averages = len(self.__averaging_weights)
            n_data_in_segment = n_data // n_averages

            fitnesses_splitted = []
            self.fitness = 0
            for i_avg, weight in enumerate(self.__averaging_weights):
                first = n_data_in_segment * i_avg
                last = first + n_data_in_segment
                data_in_segment = data.iloc[first:last, :]

                self.trader = Trader(self.__lot_size)

                # トレード
                self.trader.trade(strategy, data_in_segment)

                # 最も古いポジションを破棄
                if self.__can_abandon_the_oldest_position:
                    self.trader.abandon_the_oldest_position()

                # 建玉をクローズ
                if not self.__can_end_with_open_positions:
                    rate_last = data.iloc[-1, :]
                    closing_time = rate_last.name
                    closing_rate = rate_last[0]
                    self.trader.close_open_positions(closing_time, closing_rate)

                # 確率の計算
                self.trader.calculate_positions_probability(
                    probability_calculator, data_in_segment)

                # レバレッジの計算
                self.trader.calculate_positions_size(
                    position_size_calculator, data_in_segment)

                # 集計
                self.trader.sum_up_positions()

                fitness = self.__calculate_fitness(self.trader)
                fitnesses_splitted.append(fitness)
                self.fitness += fitness * weight

            self.fitness -= self.__rd_coeff * stdev(fitnesses_splitted)

            self.notify_observers()

            return self.fitness

        return evaluate