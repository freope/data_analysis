from frestu.feature_extraction.time_series.spectrum import ExtractorFft
from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorStft(ExtractorFeatureAbstract):

    def __init__(self, time_span, window, stride, the_last_span_is_valid=True):
        self.__time_span = time_span
        self.__window = window
        self.__stride = stride
        self.__the_last_span_is_valid = the_last_span_is_valid

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

        time_span_of_the_window = (self.__window / n_data) * self.__time_span
        extractor = ExtractorFft(time_span_of_the_window)

        q = (n_data - self.__window) // self.__stride
        r = (n_data - self.__window) % self.__stride

        spectra_amp = []
        for i in range(q+1):
            first = i * self.__stride
            last = first + self.__window
            freqs, spectrum_amp = extractor.extract(wave[first:last])
            spectra_amp.append(spectrum_amp)

        if self.__the_last_span_is_valid and r != 0:
            freqs, spectrum_amp = extractor.extract(wave[-self.__window:])
            spectra_amp.append(spectrum_amp)
        
        return freqs, spectra_amp