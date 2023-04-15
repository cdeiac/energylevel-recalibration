import datetime

import numpy as np
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from repositories.ModelRepository import ModelRepository


class ModelService:

    def __init__(self):
        self.model = None
        self.__repository = ModelRepository();

    def init_model(self):
        self.model = XGBRegressor()


    def train_model(self, df: DataFrame):
        X_train, y_train, X_test, y_test, X_val, y_val = self.__prepare_data(df)
        self.model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100)

    def predict(self, X_val, y_val):
        y_pred = self.model.predict(X_val)
        score = np.sqrt(mean_squared_error(y_val, y_pred))
        # TODO: Save score
        # TODO:


    def __prepare_data(self, df: DataFrame):
        # split today's data, it will be used for predictions
        df_historic =  df.loc[(df['timestamp'] < datetime.date.today())]
        df_today = df.loc[(df['timestamp'] == datetime.date.today())]
        # split up data
        df_train, df_test = train_test_split(df_historic, test_size=0.2)
        X_train = df_train[ df_train.columns[df_train.columns!='bodyBattery']]
        y_train = df_train['bodyBattery']
        X_test = df_test[df_test.columns[df_test.columns != 'bodyBattery']]
        y_test = df_test['bodyBattery']
        X_val = df_today[df_today.columns[df_today.columns != 'bodyBattery']]
        y_val = df_today['bodyBattery']

        return X_train, y_train, X_test, y_test, X_val, y_val


    def get_latest_model(self, userId: str):
        return self.__repository.get_latest_model(userId)