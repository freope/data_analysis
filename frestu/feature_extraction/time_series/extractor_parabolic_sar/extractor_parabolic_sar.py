import pyximport
pyximport.install()

import pandas as pd

from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series.extractor_parabolic_sar.extract_with_cython import extract_with_cython


class ExtractorParabolicSar(ExtractorFeatureAbstract):

    def __init__(
            self, step_af=0.02, af_max=0.2,
            column_name='SAR', using_cython=True):
        self.__step_af = step_af
        self.__af_max = af_max
        self.__column_name = column_name
        self.__using_cython = using_cython

    def extract(self, df):
        if self.__using_cython:
            rates = list(df.iloc[:, 0])
            sar = extract_with_cython(rates, self.__step_af, self.__af_max)
            sar = pd.DataFrame(sar, columns=[self.__column_name])
            sar.index = df.index
            return sar
        else:
            return self.__extract_with_python(
                df, self.__step_af, self.__af_max, self.__column_name)
        
    def __extract_with_python(self, df, step_af, af_max, column_name):
        # 初期化
        is_rising = True
        ix_switching = df.index[0]
        ep = df.iloc[0][0]
        ep_last = None
        af = 0
        sar = df.iloc[0][0]
        sar_last = sar
        parabolic_sar = pd.DataFrame([], columns=[column_name])

        def __update_ep(ix, df):
            nonlocal is_rising
            nonlocal ix_switching
            nonlocal ep
            
            if is_rising:
                ep = df[ix_switching:ix].max()[0]
            else:
                ep = df[ix_switching:ix].min()[0]

        def __update_af():
            nonlocal is_rising
            nonlocal ep
            nonlocal ep_last
            nonlocal af
            
            # 上昇トレンド中に EP の最大値が更新されるか、
            # 下降トレンド中に EP の最小値が更新される場合、af を更新
            if ((is_rising and ep_last < ep)
                    or (not(is_rising) and ep < ep_last)):
                af += step_af

            if af_max < af:
                af = af_max

        for ix, row in df.iterrows():
            sar_last = sar
            ep_last = ep

            # EP を更新
            __update_ep(ix, df)

            # AF を更新
            __update_af()

            # SAR を計算
            sar = (ep - sar_last) * af + sar_last

            # 上昇トレンド中に SAR がデータを超えるか、
            # 下降トレンド中に SAR がデータを下回ると切り替え
            if ((is_rising and row[0] < sar)
                    or (not(is_rising) and sar < row[0])):
                is_rising = not(is_rising)
                af = step_af
                sar = ep
                ix_switching = ix
                
            parabolic_sar.loc[ix, column_name] = sar

        return parabolic_sar