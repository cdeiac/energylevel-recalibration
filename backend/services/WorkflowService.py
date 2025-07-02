from datetime import datetime

import pandas as pd

from dtos.BodyBatteryLabel import BodyBatteryLabel
from services.ActivityService import ActivityService
from services.BodyBatteryService import BodyBatteryService
from services.SleepService import SleepService
from services.StressLevelService import StressLevelService
import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

features = [
    'sleepLevelType', 'durationInSeconds', 'activityType',  # ,'respiration'
    'averageHeartRateInBeatsPerMinute', 'averageRunCadenceInStepsPerMinute',
    'averageSpeedInMetersPerSecond', 'averagePaceInMinutesPerKilometer',
    'activeKilocalories', 'distanceInMeters',
    'maxHeartRateInBeatsPerMinute', 'maxPaceInMinutesPerKilometer',
    'maxRunCadenceInStepsPerMinute', 'maxSpeedInMetersPerSecond', 'steps',
    'totalElevationGainInMeters', 'stressLevel', 'hour', 'minute', 'dayOfYear', 'dayOfMonth']
target = 'bodyBattery'


class WorkflowService:
    """
    Workflow service responsible for training an XGBoost model on multi-source wellness data
    and generating predictions for Body Battery levels.

    Combines granular and interval-based data sources, preprocesses them, performs feature
    engineering, trains the model, and applies predictions.
    """

    def __init__(self):
        """
        Initializes the workflow with required services, repositories, and model configuration.
        """
        self.granular_data_repositories = [
            BodyBatteryService(),
            StressLevelService(),
        ]
        self.interval_data_repositories = [
            SleepService(),
            ActivityService()
        ]
        self.data = []
        self.interval_data = []
        self.labelEncoder = LabelEncoder()
        self.model = xgb.XGBRegressor(n_estimators=1000, early_stopping_rounds=100)

    async def train(self, userId: str):
        """
        Executes the full training pipeline for a user:
        - Loads data
        - Prepares and encodes features
        - Trains the model
        - Predicts Body Battery values
        - Stores predictions

        Parameters:
        -----------
        userId : str
            The user for whom the model is being trained and applied.
        """
        await self.__get_all_data(userId=userId)
        df = self.__prepare_data()
        df = self.__augment_features(df)
        df = self.__encode_categorical_features(df)

        X_train, y_train, X_test, y_test = self.__train_test_split(df)
        self.__init_train_predict(X_train, y_train, X_test, y_test)

        df = self.__add_new_predictions(df)
        data = await self.granular_data_repositories[0].find_all(userId)

        prediction_labels = []
        prev_prediction = None
        for entry in data:
            row = df.loc[df['timestamp'] == datetime.fromtimestamp(entry.timestamp)]['prediction']
            if not row.empty:
                prediction = int(row.values[0])
                entry.prediction = prediction
                prev_prediction = prediction
            else:
                entry.prediction = prev_prediction
            prediction_labels.append(BodyBatteryLabel(timestamp=entry.timestamp, label=entry.prediction))

        await self.granular_data_repositories[0].add_body_battery_predictions(userId, prediction_labels)
        return

    def __add_new_predictions(self, df):
        """
        Generates predictions on the full dataset using the trained model.

        Parameters:
        -----------
        df : DataFrame
            The preprocessed feature set.

        Returns:
        --------
        DataFrame
            The original DataFrame with an added 'prediction' column.
        """
        X = df[features]
        y_pred = self.model.predict(X)
        df['prediction'] = y_pred
        return df

    def __init_train_predict(self, X_train, y_train, X_test, y_test):
        """
        Trains the model and prints performance on the test set.

        Parameters:
        -----------
        X_train, y_train, X_test, y_test : DataFrame
            The training and test features/targets.
        """
        self.model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100)
        y_pred = self.model.predict(X_test)
        score = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f'RMSE Score on Test set: {score:0.2f}')

    @staticmethod
    def __train_test_split(df):
        """
        Splits the dataset into train and test partitions using a static timestamp cutoff.

        Returns:
        --------
        Tuple
            X_train, y_train, X_test, y_test
        """
        train = df.loc[df.timestamp < pd.to_datetime("2023-01-25 00:00:00")]
        test = df.loc[df.timestamp >= pd.to_datetime("2023-01-25 00:00:00")]

        X_train = train[features]
        y_train = train[target]
        X_test = test[features]
        y_test = test[target]

        return X_train, y_train, X_test, y_test

    def __encode_categorical_features(self, df):
        """
        Encodes categorical variables (e.g. sleep level, activity type) using label encoding.

        Parameters:
        -----------
        df : DataFrame
            Input dataset with categorical features.

        Returns:
        --------
        DataFrame
            Dataset with encoded categorical features.
        """
        df.sleepLevelType = self.labelEncoder.fit_transform(df.sleepLevelType.values)
        df.activityType = self.labelEncoder.fit_transform(df.activityType.values)
        return df

    def __augment_features(self, df):
        """
        Adds temporal features derived from the 'timestamp' column.

        Returns:
        --------
        DataFrame
            Enriched feature set with columns like hour, dayOfYear, etc.
        """
        df = df.copy()
        df['hour'] = df.timestamp.dt.hour
        df['minute'] = df.timestamp.dt.minute
        df['dayOfYear'] = df.timestamp.dt.dayofyear
        df['dayOfMonth'] = df.timestamp.dt.day
        return df

    async def __get_all_data(self, userId: str):
        """
        Loads all required user data from granular and interval repositories.

        Parameters:
        -----------
        userId : str
            The user whose data should be fetched.

        Returns:
        --------
        List[DataFrame]
            A list of DataFrames with the raw data.
        """
        for repo in self.granular_data_repositories:
            self.data.append(await repo.find_all_to_dataframe(userId))
        for repo in self.interval_data_repositories:
            self.interval_data.append(await repo.find_all_to_dataframe(userId))
        return self.data

    @staticmethod
    def __function(x, df1):
        """
        Helper function to clean/resample time intervals for alignment with 15-minute bins.

        Parameters:
        -----------
        x : Series
            A row of the interval DataFrame.
        df1 : DataFrame
            Reference DataFrame used for comparison.
        """
        if x.name < df1.shape[0]:
            x.timeEnd = x.timeStart + pd.Timedelta("15min")
        else:
            x.timeStart = x.timeEnd - pd.Timedelta("15min")
        return x

    def __prepare_data(self):
        """
        Prepares the final training dataset by joining and resampling all available sources.

        Returns:
        --------
        DataFrame
            A fully merged and time-aligned dataset with all features.
        """
        df = None
        for entry in self.data:
            df = entry if df is None else pd.merge(df, entry)

        for intv_entry in self.interval_data:
            df = df.sort_values(by='timestamp')
            intv_entry = intv_entry.sort_values(by='timeStart')
            intv_entry = intv_entry.drop_duplicates(subset='timeStart', keep='first')
            intv_entry = intv_entry.drop_duplicates(subset='timeEnd', keep='first')

            df1 = intv_entry.set_index("timeStart").resample("15min").pad().reset_index()
            df2 = intv_entry.set_index("timeEnd").resample("15min").bfill().reset_index()
            df3 = pd.concat([df1, df2], ignore_index=True)

            df_resampled = df3[df3.timeStart < df3.timeEnd].apply(lambda x: self.__function(x, df1), axis=1)
            df_resampled = df_resampled.drop('timeEnd', axis=1)
            df_resampled = df_resampled.rename(columns={'timeStart': 'timestamp'})

            df = pd.merge(df, df_resampled, how="left", on=["timestamp", "calendarDate", "dayOfWeek", "month"])

        df = df.drop_duplicates(subset=["timestamp"], keep=False)
        return df
