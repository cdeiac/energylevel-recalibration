import logging
from pydantic.schema import date
from mappings.RespirationMapper import RespirationMapper
from repositories.RespirationRepository import RespirationRepository
from schemas.Respiration import Respiration


class RespirationService:
    """
    Service layer for handling operations related to respiration data, including:
    - Saving mapped DTO data
    - Retrieving data by user and date range
    - Converting data into a pandas DataFrame for analysis
    """

    __log = logging.getLogger(__name__)
    __repository = RespirationRepository()

    async def save_many(self, respirationDetails):
        """
        Processes and saves multiple respiration data entries, filtered to 15-minute intervals.

        Parameters:
        -----------
        respirationDetails : RespirationDetails
            DTO containing all-day respiration data with epoch-to-breath mappings.

        Returns:
        --------
        RespirationDetails
            The original DTO after saving its mapped entries.
        """
        if not respirationDetails.allDayRespiration:
            return {}

        respirationEntries = []
        for respiration in respirationDetails.allDayRespiration:
            for key, value in respiration.timeOffsetEpochToBreaths.items():
                if int(key) % 900 == 0:  # Save every 15 minutes
                    respirationEntry = RespirationMapper.from_respiration_detail(respiration, key, value).to_json()
                    self.__log.debug(respirationEntry)
                    respirationEntries.append(respirationEntry)

        await self.__repository.save_many(sorted(respirationEntries, key=lambda e: e['timestamp']))
        return respirationDetails

    async def find_many(self, userId: str, dateStart: date, dateEnd: date):
        """
        Retrieves respiration entries for a user within a specified date range.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        dateStart : date
            The start date of the range (inclusive).
        dateEnd : date
            The end date of the range (exclusive).

        Returns:
        --------
        List[Respiration]
            A list of parsed Respiration objects.
        """
        if not dateStart <= dateEnd:
            raise ValueError('dateStart must be before dateEnd!')

        result = await self.__repository.find_many(userId, dateStart, dateEnd)
        return [Respiration.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        """
        Retrieves all respiration records for a given user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[Respiration]
            All parsed respiration records for the user.
        """
        result = await self.__repository.find_all(userId)
        return [Respiration.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        """
        Retrieves all respiration data for a user and converts it into a pandas DataFrame.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        DataFrame
            A structured DataFrame of respiration values.
        """
        result = await self.find_all(userId)
        return RespirationMapper.to_dataframe(data=result)
