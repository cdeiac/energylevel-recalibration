import logging
from datetime import datetime, timedelta
from pydantic.schema import date

from mappings import SleepMapper
from mappings.SleepMapper import SleepMapper
from dtos.sleep import Sleeps
from repositories.SleepRepository import SleepRepository
from repositories.SleepStatisticsRepository import SleepStatisticsRepository
from schemas.Sleep import Sleep
from schemas.SleepStatistics import SleepStatistics


class SleepService:
    """
    Service layer for managing sleep and sleep statistics data.
    Handles ingestion, transformation, retrieval, and export of sleep-related records.
    """

    __log = logging.getLogger(__name__)
    __repository = SleepRepository()
    __statsRepository = SleepStatisticsRepository()

    async def save_many(self, sleeps: Sleeps):
        """
        Saves sleep records and statistics to their respective repositories.

        Parameters:
        -----------
        sleeps : Sleeps
            A DTO containing multiple sleep sessions and their detailed levels.

        Returns:
        --------
        List[dict]
            A list of saved sleep entries in JSON format.
        """
        if not sleeps.sleeps:
            return {}

        mapped_entries = []
        mapped_stats_entries = []

        for sleep in sleeps.sleeps:
            mapped_stats_entries.append(SleepMapper.to_sleep_stats(sleep).to_json())
            for sleepLevelTuple in sleep.sleepLevelsMap:
                if not sleepLevelTuple:
                    continue
                sleep_level_type = sleepLevelTuple[0]
                sleep_level_entries = sleepLevelTuple[1]
                if not sleep_level_entries:
                    continue
                for entry in sleep_level_entries:
                    mapped_entry = SleepMapper.from_sleep(sleep, entry, sleep_level_type).to_json()
                    self.__log.debug(mapped_entry)
                    mapped_entries.append(mapped_entry)

        await self.__repository.save_many(mapped_entries)
        await self.__statsRepository.save_many(mapped_stats_entries)
        return mapped_entries

    async def find_one_statistic(self, userId: str, targetDate: date):
        """
        Retrieves sleep statistics for a specific user on a given date.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        targetDate : date
            The target calendar date.

        Returns:
        --------
        List[SleepStatistics]
            A list of matching sleep statistics entries.
        """
        targetDate = datetime.fromisoformat(targetDate.isoformat())
        result = await self.__statsRepository.find_one(userId, targetDate)
        return [SleepStatistics.parse_obj(res) for res in result]

    async def find_many(self, userId: str, start: int, end: int):
        """
        Retrieves sleep records for a user within a given time range.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        start : int
            Start timestamp (epoch seconds).
        end : int
            End timestamp (epoch seconds).

        Returns:
        --------
        List[Sleep]
            A list of sleep entries.
        """
        if not start <= end:
            raise ValueError('dateStart must be before dateEnd!')

        result = await self.__repository.find_many(userId, start, end)
        return [Sleep.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        """
        Retrieves all sleep records for a user.

        Parameters:
        -----------
        userId : str

        Returns:
        --------
        List[Sleep]
        """
        result = await self.__repository.find_all(userId)
        return [Sleep.parse_obj(res) for res in result]

    async def find_all_statistics(self, userId: str):
        """
        Retrieves all sleep statistics for a user.

        Parameters:
        -----------
        userId : str

        Returns:
        --------
        List[SleepStatistics]
        """
        result = await self.__statsRepository.find_all(userId)
        return [SleepStatistics.parse_obj(res) for res in result]

    async def find_many_statistics(self, userId: str, start: int, end: int):
        """
        Retrieves sleep statistics for a user over a time range.

        Parameters:
        -----------
        userId : str
        start : int
        end : int

        Returns:
        --------
        List[SleepStatistics]
        """
        result = await self.__statsRepository.find_many(userId, start, end)
        return [SleepStatistics.parse_obj(res) for res in result]

    async def find_awake_time(self, userId: str, targetDate: date):
        """
        Estimates awake time for a user on a given day by examining sleep statistics
        of that day and the following day.

        Parameters:
        -----------
        userId : str
        targetDate : date

        Returns:
        --------
        List[float]
            A list containing the start time of sleep before and after the target date.
        """
        target_date = datetime.fromisoformat(targetDate.isoformat())
        tomorrow_date = target_date + timedelta(days=1)

        sleep_time_previous_day = await self.__statsRepository.find_one(userId, target_date)
        sleep_time_current_day = await self.__statsRepository.find_one(userId, tomorrow_date)

        sleeps_prev = [SleepStatistics.parse_obj(res) for res in sleep_time_previous_day]
        sleeps_curr = [SleepStatistics.parse_obj(res) for res in sleep_time_current_day]

        sleep_time = []
        if sleeps_prev:
            sleep_time.append(sleeps_prev[0].startTimeOffsetInSeconds)
        else:
            sleep_time.append(target_date.timestamp())
        if sleeps_curr:
            sleep_time.append(sleeps_curr[0].startTimeOffsetInSeconds)
        else:
            sleep_time.append(tomorrow_date.timestamp())

        return sleep_time

    async def find_all_to_dataframe(self, userId: str):
        """
        Retrieves all sleep records for a user and converts them to a DataFrame.

        Parameters:
        -----------
        userId : str

        Returns:
        --------
        DataFrame
        """
        result = await self.find_all(userId)
        return SleepMapper.to_dataframe(data=result)
