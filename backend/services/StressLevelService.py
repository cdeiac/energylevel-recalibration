import logging
from mappings.StressLevelMapper import StressLevelMapper
from repositories.StressLevelRepository import StressLevelRepository
from schemas.stress import StressLevel


class StressLevelService:
    """
    Service layer for handling operations related to user stress level data.
    Supports saving new entries, retrieving data, and converting results into a DataFrame.
    """

    __log = logging.getLogger(__name__)
    __repository = StressLevelRepository()

    async def save_many(self, stressDetails):
        """
        Saves multiple stress level entries from DTO, filtered to 15-minute intervals.

        Parameters:
        -----------
        stressDetails : StressDetails
            DTO containing stress level values mapped by timestamp offset.

        Returns:
        --------
        StressDetails
            The original input after processing and saving entries.
        """
        if not stressDetails.stressDetails:
            return {}

        stressEntries = []
        for stressDetail in stressDetails.stressDetails:
            for key, value in stressDetail.timeOffsetStressLevelValues.items():
                if int(key) % 900 == 0:  # Save every 15 minutes
                    stressEntry = StressLevelMapper.from_stress_detail(stressDetail, key, value).to_json()
                    self.__log.debug(stressEntry)
                    stressEntries.append(stressEntry)

        await self.__repository.save_many(sorted(stressEntries, key=lambda e: e['timestamp']))
        return stressDetails

    async def find_many(self, userId: str, start: int, end: int):
        """
        Retrieves stress level records within a specified time range for a user.

        Parameters:
        -----------
        userId : str
            The unique identifier of the user.
        start : int
            Start time in epoch seconds (inclusive).
        end : int
            End time in epoch seconds (inclusive).

        Returns:
        --------
        List[StressLevel]
            A list of parsed stress level entries.
        """
        if not start <= end:
            raise ValueError('timeStart must be before timeEnd!')

        result = await self.__repository.find_many(userId, start, end)
        return [StressLevel.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        """
        Retrieves all stress level records for a user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[StressLevel]
            All stress entries for the specified user.
        """
        result = await self.__repository.find_all(userId)
        return [StressLevel.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        """
        Retrieves all stress data for a user and returns it as a pandas DataFrame.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        DataFrame
            Structured stress data including timestamp, value, and calendar info.
        """
        result = await self.find_all(userId)
        return StressLevelMapper.to_dataframe(data=result)
