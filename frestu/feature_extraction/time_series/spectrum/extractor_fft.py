import numpy as np

from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorFft(ExtractorFeatureAbstract):

    def __init__(self, time_span):
        self.__time_span = time_span
    
    def extract(self, wave):
        """
        振幅スペクトルを抽出

        Parameters
        ----------
        wave : numpy.ndarray, pandas.core.series.Series
            スペクトル解析対象の波。データフレームではないことに注意。

        Returns
        -------
        freqs : numpy.ndarray
            周波数スケール
        spectrum_amp : numpy.ndarray
            振幅スペクトル
        """
        n_data = wave.shape[0]
        n_data_half = n_data // 2

        # サンプリング周期
        sampling_period = self.__time_span / n_data
        # サンプリング周波数
        sampling_rate = 1 / sampling_period

        # ナイキスト周波数
        nyquist = sampling_rate / 2

        # 周波数スケール
        freqs = np.fft.fftfreq(n_data, sampling_period)

        # フーリエ変換
        spectrum_complex = np.fft.fft(wave)
        # 正規化
        spectrum_complex = spectrum_complex / n_data_half
        # ローパスフィルタ
        spectrum_complex[(freqs > nyquist)] = 0

        # 振幅スペクトル
        spectrum_amp = np.abs(spectrum_complex)

        # ナイキスト周波数までに限定
        freqs = freqs[1:n_data_half]
        spectrum_amp = spectrum_amp[1:n_data_half]

        return freqs, spectrum_amp