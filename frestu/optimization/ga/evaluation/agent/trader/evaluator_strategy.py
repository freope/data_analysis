import copy

from frestu.agent.trader import Trader
from frestu.optimization.ga.evaluation import EvaluatorAbstract


class EvaluatorStrategy(EvaluatorAbstract):

    def __init__(
            self,
            strategy_class,
            translate_chromosome,
            calculate_fitness,
            probability_calculator_class=None,
            leverage_calculator_class=None):
        super().__init__()
        self.__strategy_class = strategy_class
        self.__translate_chromosome = translate_chromosome
        self.__calculate_fitness = calculate_fitness
        self.__probability_calculator_class = probability_calculator_class
        self.__leverage_calculator_class = leverage_calculator_class
        # Observer で参照するための変数
        # 遺伝子間で共有するので、並列評価では、正確な値を算出できないので注意。
        self.chromosome = None
        self.trader = None
        self.fitness = None
    
    def create_evaluating_strategy(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため
            chrom = copy.copy(chromosome)
            
            # 翻訳
            params_strategy = self.__translate_chromosome(chromosome)

            strategy = self.__strategy_class(**params_strategy)

            self.trader = Trader()
            # トレード
            self.trader.trade(strategy, data)
            # 集計
            self.trader.sum_up_positions()

            self.fitness = self.__calculate_fitness(self.trader)

            self.notify_observers()

            return self.fitness
        
        return evaluate
    
    def create_evaluating_strategy_leverage(self, data):
        def evaluate(chromosome):
            self.chromosome = chromosome

            # translate_chromosome に chromosome を破壊する操作が含まれ得るため
            chrom = copy.copy(chromosome)
            
            # 翻訳
            params_strategy, \
            params_probability, \
            params_leverage = self.__translate_chromosome(chromosome)

            strategy = self.__strategy_class(**params_strategy)

            self.trader = Trader()
            # トレード
            self.trader.trade(strategy, data)
            # 確率の計算
            pc = self.__probability_calculator_class(**params_probability)
            self.trader.calculate_positions_probability(pc, data)
            # レバレッジの計算
            lc = self.__leverage_calculator_class(**params_leverage)
            self.trader.calculate_positions_leverage(lc, data)
            # 集計
            self.trader.sum_up_positions()

            self.fitness = self.__calculate_fitness(self.trader)

            self.notify_observers()

            return self.fitness
        
        return evaluate
