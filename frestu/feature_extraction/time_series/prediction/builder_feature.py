import pandas as pd


class BuilderFeature:

    def __init__(
            self,
            future_step, features_shifts_internal,
            features_shifts_external=[], features_shifts_mixed=[]):
        self.__FEATURE_TYPE = {'internal': 0, 'external': 1, 'mixed': 2}

        self.__future_step = future_step
        self.__future_counter = 0

        self.__features_shifts_internal = features_shifts_internal
        self.__features_shifts_external = features_shifts_external
        self.__features_shifts_mixed = features_shifts_mixed
        
        self.__n_features_internal = 0
        self.__n_features_external = 0
        self.__n_features_mixed = 0

        self.__features_internal = None
        self.__features_external = None
        self.__features_mixed = None

        self.__features = []
        self.__features_rebuilt = []

    @property
    def future_shift(self):
        return self.__future_step * self.__future_counter

    @property
    def features(self):
        i_future = self.future_shift
        return self.__get_features(i_future)

    def build(self, df_internal, df_external=None):
        """
        Notes
        -----
        - df_internal, df_external は時刻が揃っている必要がある。
        - rebuild のそれらとも時刻が揃っている必要がある。
        """
        self.__features_internal = self._make_features_internal(df_internal)
        self.__features_external = self._make_features_external(df_external)
        self.__features_mixed = self._make_features_mixed(
            df_internal, df_external)
        
        self.__n_features_internal = self.__features_internal.shape[1]
        self.__n_features_external = self.__features_external.shape[1]
        self.__n_features_mixed = self.__features_mixed.shape[1]
        
        self.__features.append([{} for _ in range(self.__n_features_internal)])
        self.__features.append([{} for _ in range(self.__n_features_external)])
        self.__features.append([{} for _ in range(self.__n_features_mixed)])
        
        self.reset_rebuilding()

    def rebuild(self, df_internal, df_external=None):
        """
        Notes
        -----
        - df_internal, df_external は時刻が揃っている必要がある。
        - build のそれらとも時刻が揃っている必要がある。
        - 時刻は揃っているが rebuild する毎に、値は self.__future_step だけ先のもの
          になっている必要がある。更新された df_internal に合わせて df_external も
          更新されたものになっている必要がある。
        """
        self.__future_counter += 1

        # NOTE: features_external は rebuild 毎に同じ計算をし、無駄になり得る。
        features_internal = self._make_features_internal(df_internal)
        features_external = self._make_features_external(df_external)
        features_mixed = self._make_features_mixed(df_internal, df_external)

        i_future = self.future_shift
        
        # internal
        for i_feature in range(self.__n_features_internal):
            self.__features_rebuilt[self.__FEATURE_TYPE['internal']]\
                [i_feature][i_future] = features_internal.iloc[:, i_feature]
        
        # external
        for i_feature in range(self.__n_features_external):
            self.__features_rebuilt[self.__FEATURE_TYPE['external']]\
                [i_feature][i_future] = features_external.iloc[:, i_feature]
        
        # mixed
        for i_feature in range(self.__n_features_mixed):
            self.__features_rebuilt[self.__FEATURE_TYPE['mixed']]\
                [i_feature][i_future] = features_mixed.iloc[:, i_feature]

    def reset_rebuilding(self):
        self.__future_counter = 0
        self.__features_rebuilt.append(
            [{} for _ in range(self.__n_features_internal)])
        self.__features_rebuilt.append(
            [{} for _ in range(self.__n_features_external)])
        self.__features_rebuilt.append(
            [{} for _ in range(self.__n_features_mixed)])
    
    def __make_feature(self, feature_id):
        feature_type, i_feature, i_shift = feature_id

        # 実測値を使う場合
        if i_shift <= 0 and feature_type == self.__FEATURE_TYPE['internal']:
            return self.__features_internal.iloc[:, i_feature].shift(-i_shift)

        if i_shift <= 0 and feature_type == self.__FEATURE_TYPE['external']:
            return self.__features_external.iloc[:, i_feature].shift(-i_shift)
        
        if i_shift <= 0 and feature_type == self.__FEATURE_TYPE['mixed']:
            return self.__features_mixed.iloc[:, i_feature].shift(-i_shift)

        # 予測値を使う場合
        i_shift_base = (i_shift // self.__future_step + 1) * self.__future_step\
            if i_shift % self.__future_step != 0 else i_shift

        i_shift_diff = i_shift_base - i_shift

        feature = self.__features_rebuilt[feature_type][i_feature][i_shift_base]
        # NOTE: ここで 現在に近い未来の部分に NaN が入るので fillna した方が良いかも。
        feature = feature.shift(i_shift_diff)

        return feature
        
    def __get_feature(self, feature_id):
        feature_type, i_feature, i_shift = feature_id
        
        # 取得したい特徴がなければ作成
        if not i_shift in self.__features[feature_type][i_feature]:
            self.__features[feature_type][i_feature][i_shift] = \
                self.__make_feature(feature_id)
        
        return self.__features[feature_type][i_feature][i_shift]

    def __get_features_id(self, i_future):
        features_id = []

        # internal
        for i_feature, i_shifts in enumerate(self.__features_shifts_internal):
            for i_shift in i_shifts:
                features_id.append([
                    self.__FEATURE_TYPE['internal'],
                    i_feature,
                    i_future - i_shift])

        # external
        for i_feature, i_shifts in enumerate(self.__features_shifts_external):
            for i_shift in i_shifts:
                features_id.append([
                    self.__FEATURE_TYPE['external'],
                    i_feature,
                    i_future - i_shift])

        # mixed
        for i_feature, i_shifts in enumerate(self.__features_shifts_mixed):
            for i_shift in i_shifts:
                features_id.append([
                    self.__FEATURE_TYPE['mixed'],
                    i_feature,
                    i_future - i_shift])
        
        return features_id

    def __get_features(self, i_future):
        features_id = self.__get_features_id(i_future)

        features = [self.__get_feature(feature_id)
            for feature_id in features_id]
            
        features_name = ['_'.join([str(i) for i in feature_id])
            for feature_id in features_id]

        features = pd.concat(features, axis=1)
        features.columns = features_name
        
        return features

    def _make_features_internal(self, df):
        return df
    
    def _make_features_external(self, df):
        return pd.DataFrame()
    
    def _make_features_mixed(self, df_internal, df_external):
        return pd.DataFrame()