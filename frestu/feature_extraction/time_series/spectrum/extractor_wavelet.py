import matplotlib.pyplot as plt
import numpy as np
import pywt

from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorWavelet(ExtractorFeatureAbstract):
    """
    Notes
    -----
    - mexican hat wavelet "mexh"
    - Morlet wavelet "morl"
    - complex Morlet wavelet
      ("cmorB-C" with floating point values B, C)
    - Gaussian wavelets
      ("gausP" where P is an integer between 1 and and 8)
    - complex Gaussian wavelets
      ("cgauP" where P is an integer between 1 and 8)
    - Shannon wavelets
      ("shanB-C" with floating point values B and C)
    - frequency B-spline wavelets
      ("fpspM-B-C" with integer M and floating point B, C)

    References
    ----------
    https://pywavelets.readthedocs.io/en/latest/ref/cwt.html
    """

    def __init__(
          self, time_span, freq_min, n_scales, mother_wavelet='cmor1.5-1.0'):
        self.__time_span = time_span
        self.__n_scales = n_scales
        self.__freq_min = freq_min
        self.__mother_wavelet = mother_wavelet
    
    def extract(self, wave):
        """
        振幅スペクトルの時系列を抽出

        Parameters
        ----------
        wave : numpy.ndarray, pandas.core.series.Series
            スペクトル解析対象の波。データフレームではないことに注意。

        Returns
        -------
        freqs : numpy.ndarray
            周波数スケール
        spectra_amp : list of numpy.ndarray
            振幅スペクトルの時系列
        """
        n_data = wave.shape[0]
        n_data_half = n_data // 2

        # サンプリング周期
        sampling_period = self.__time_span / n_data
        # サンプリング周波数
        sampling_rate = 1 / sampling_period

        # ナイキスト周波数
        nyquist = sampling_rate / 2

        if not self.__freq_min < nyquist:
            raise ValueError('shoulde be freq_min < nyquist.')

        # cmor 基準で考えた、解析したい周波数のリスト（ナイキスト周波数以下）
        freqs_cmor = np.linspace(self.__freq_min, nyquist, self.__n_scales)

        # スケール
        scales = sampling_rate / freqs_cmor

        # NOTE: freqs_rate だけ個別に計算することも可能
        # freqs_rate = pywt.scale2frequency(
        #     scale=scales, wavelet=self.__mother_wavelet)

        # ウェーブレッド変換
        spectra_complex, freqs_rate = pywt.cwt(
            wave, scales=scales, wavelet=self.__mother_wavelet)

        # mother_wavelet に対応した周波数を計算
        freqs = freqs_rate / sampling_period

        # 振幅スペクトル
        spectra_amp = np.abs(spectra_complex)

        return freqs, spectra_amp

    @staticmethod
    def get_mother_wavelets():
        return pywt.wavelist(kind='continuous')
    
    @staticmethod
    def show_mother_wavelet(mother_wavelet, precision=8, figsize=(8, 5)):
        wavelet = pywt.ContinuousWavelet(mother_wavelet)
        int_psi, x = pywt.integrate_wavelet(wavelet, precision=precision)
        plt.figure(figsize=figsize)
        plt.plot(x, int_psi)
        plt.show()