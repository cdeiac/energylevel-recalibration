import datetime

import numpy as np
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from repositories.ModelRepository import ModelRepository


class ModelService:
    """
    Service class for initializing, training, evaluating, and retrieving machine learning models.
    Currently uses XGBoost for regression on body battery data.
    """

    def __init__(self):
        """
        Initializes the ModelService with a placeholder for the model and a reference to the model repository.
        """
        self.model = None
        self.__repository = ModelRepository()

    def init_model(self):
        """
        Initializes a new instance of the XGBRegressor model.
        """
        self.model = XGBRegressor()

    def train_model(self, df: DataFrame):
        """
        Trains the XGBoost model on historical body battery data.

        Parameters:
        -----------
        df : DataFrame
            A pandas DataFrame containing the body battery data with a 'bodyBattery' target column.
        """
        X_train, y_train, X_test, y_test, X_val, y_val = self.__prepare_data(df)
        self.model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100)

    def predict(self, X_val, y_val):
        """
        Makes predictions using the trained model and evaluates performance on validation data.

        Parameters:
        -----------
        X_val : DataFrame
            The features for the validation set.
        y_val : Series or array-like
            The true target values for validation.

        Returns:
        --------
        None
        """
        y_pred = self.model.predict(X_val)
        score = np.sqrt(mean_squared_error(y_val, y_pred))
        # TODO: Save score
        # TODO: Return or log predictions/results

    def __prepare_data(self, df: DataFrame):
        """
        Splits the input DataFrame into training, testing, and validation sets.
        Today's data is used for validation; the rest is split into training and testing.

        Parameters:
        -----------
        df : DataFrame
            The input DataFrame with a 'timestamp' column and a 'bodyBattery' target.

        Returns:
        --------
        Tuple of train/test/validation splits:
            X_train, y_train, X_test, y_test, X_val, y_val
        """
        df_historic = df.loc[(df['timestamp'] < datetime.date.today())]
        df_today = df.loc[(df['timestamp'] == datetime.date.today())]
        df_train, df_test = train_test_split(df_historic, test_size=0.2)

        X_train = df_train[df_train.columns[df_train.columns != 'bodyBattery']]
        y_train = df_train['bodyBattery']
        X_test = df_test[df_test.columns[df_test.columns != 'bodyBattery']]
        y_test = df_test['bodyBattery']
        X_val = df_today[df_today.columns[df_today.columns != 'bodyBattery']]
        y_val = df_today['bodyBattery']

        return X_train, y_train, X_test, y_test, X_val, y_val

    def get_latest_model(self, userId: str):
        """
        Retrieves the most recently saved model for the given user from the model repository.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        XGBRegressor
            The latest XGBoost model associated with the user.
        """
        return self.__repository.get_latest_model(userId)
