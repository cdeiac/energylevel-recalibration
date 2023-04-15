import pandas as pd
from fastapi.encoders import jsonable_encoder
from pandas import DataFrame

from services.ActivityService import ActivityService
from services.BodyBatteryService import BodyBatteryService
from services.RespirationService import RespirationService
from services.SleepService import SleepService
from services.StepsService import StepsService
from services.StressLevelService import StressLevelService


class WorkflowService:

    def __init__(self):
        # data with a granularity of 3 min
        self.granular_data_repositories = [
            BodyBatteryService(),
            RespirationService(),
            StressLevelService(),
            #StepsService() gather steps directly from activity
        ]
        # interval data
        self.interval_data_repositories = [
            SleepService(),
            ActivityService()
        ]
        self.data = []
        self.interval_data = []

    async def get_all_data(self, userId: str):
        await self.__get_all_data(userId=userId)
        df = self.__prepare_data()
        print(df)


    async def __get_all_data(self, userId: str):
        """
        Gathers all the relevant data that will be used to train the model

        Args:
            userId: User reference
        """
        # gather data
        for repo in self.granular_data_repositories:
            self.data.append(await repo.find_all_to_dataframe(userId))
        # need to treat interval data separately
        for repo in self.interval_data_repositories:
            self.interval_data.append(await repo.find_all_to_dataframe(userId))

        resampled_data = []
        #for repo in self.interval_data_repositories:
            # interval data
            #interval_data = await repo.find_all(userId)
            ##for entry in interval_data:
                #current_timestamp = entry['startTimeOffsetInSeconds']
                #while current_timestamp <= entry['endTimeOffsetInSeconds']:
                #    # add data in 3 minutes interval to match other data
                #    entry['timestamp'] = current_timestamp
                #    resampled_data.append(entry)
                #    current_timestamp += 180
            # add resampled data
            #self.data.append(resampled_data)
        return self.data


    def __prepare_data(self):
        """
        Prepares the gathered data for the ML task in a dataframe

        Returns:
            the joined dataset in the form of a dataframe
        """
        df = None
        for entry in self.data:
            # Merge the two dataframes based on time column
            if df is None:
                df = entry
            else:
                #df = pd.join(df, entry, on='timestamp')
                df = pd.concat([df, entry], axis=0)

            #df_new = pd.DataFrame(jsonable_encoder(objects))
            #df_new = pd.Index([s.__dict__ for s in objects]).to_frame()

            #print(df_new.columns)
            #if 'bodyBattery' in df_new['dateType'].tolist():
            #    df_new.rename(columns={'value': 'bodyBattery'}, inplace=True)
            #print(df_new)

        for intv_entry in self.interval_data:
            # merging requires sorting
            df = df.sort_values(by='timestamp')
            #df.set_index('timestamp', inplace=True)
            #intv_entry.set_index('timeStart', inplace=True)
            intv_entry = intv_entry.sort_values(by='timeStart')
            #resampled_series = intv_entry.resample('3min', on='timeStart',).bfill()
            # merge dataframes by time
            # Merge the two dataframes based on time column
            #df = pd.merge_asof(df, intv_entry, left_on='timeStart', right_on='timeEnd', direction='backward')
            df = pd.merge_asof(df, intv_entry, left_on='timestamp', right_on='timeStart', direction='backward')
            # Filter the merged dataframe to keep rows where time is between start_time and end_time
            #df = df[(df['timestamp'] >= df['timeStart']) & (df['timestamp'] <= df['timeEnd'])]
        return df
