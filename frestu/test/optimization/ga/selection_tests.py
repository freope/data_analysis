import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.selection import *


class SelectionTests(unittest.TestCase):

    def setUp(self):
        self.vec_1 = np.array([100, 80, 60, 40, 20])
        self.vec_2 = np.array([-20, -40, -60, -80, -100])
    
    def tearDown(self):
        pass
    
    def test_select_roulette(self):
        # HACK: 出現回数の大小しかテストしていない。
        # NOTE: 3000 回試行しているが、小さい確率でテストに失敗しうる。
        # vec_1 に対してテスト
        counts = pd.DataFrame(
            [select_roulette(self.vec_1) for _ in range(3000)],
            columns=['val']).groupby('val')['val'].count()
        for i in range(len(counts)-1):
            self.assertGreater(counts[i], counts[i+1])
        # vec_2 に対してテスト
        counts = pd.DataFrame(
            [select_roulette(self.vec_2) for _ in range(3000)],
            columns=['val']).groupby('val')['val'].count()
        for i in range(len(counts)-1):
            self.assertGreater(counts[i], counts[i+1])
    
    def test_select_ranking(self):
        # HACK: 出現回数の大小しかテストしていない。
        # NOTE: 3000 回試行しているが、小さい確率でテストに失敗しうる。
        # vec_1 に対してテスト
        counts = pd.DataFrame(
            [select_ranking(self.vec_1) for _ in range(3000)],
            columns=['val']).groupby('val')['val'].count()
        for i in range(len(counts)-1):
            self.assertGreater(counts[i], counts[i+1])
        # vec_2 に対してテスト
        counts = pd.DataFrame(
            [select_ranking(self.vec_2) for _ in range(3000)],
            columns=['val']).groupby('val')['val'].count()
        for i in range(len(counts)-1):
            self.assertGreater(counts[i], counts[i+1])

    def test_select_tournament(self):
        pass


if __name__ == '__main__':
    unittest.main()