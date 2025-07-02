import datetime
import logging
from mappings.StepsMapper import StepsMapper
from repositories.StepsRepository import StepsRepository
from schemas.Steps import Steps


class StepsService:
    """
    Service class for managing user step data.
    Provides methods to fetch, parse, and transform step entries.
    """

    __log = logging.getLogger(__name__)
    __steps_repository = StepsRepository()

    async def find_many(self, userId: str, timeStart: datetime, timeEnd: datetime):
        """
        Retrieves step records for a user between two timestamps.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        timeStart : datetime
            Start of the time range (inclusive).
        timeEnd : datetime
            End of the time range (inclusive).

        Returns:
        --------
        List[Steps]
            Parsed step entries within the specified time range.
        """
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        result = await self.__steps_repository.find(userId, timeStart, timeEnd)
        return [Steps.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        """
        Retrieves all step records for a specific user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[Steps]
            All parsed step entries for the user.
        """
        result = await self.__steps_repository.find_all(userId)
        return [Steps.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        """
        Retrieves all step records for a user and converts them into a pandas DataFrame.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        DataFrame
            Structured step data in tabular format.
        """
        result = await self.find_all(userId)
        return StepsMapper.to_dataframe(data=result)
