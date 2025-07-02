import logging
from typing import List
from mappings.BodyBatteryMapper import BodyBatteryMapper
from repositories.BodyBatteryLabelsRepository import BodyBatteryLabelsRepository
from repositories.BodyBatteryRepository import BodyBatteryRepository
from dtos.BodyBatteryLabel import BodyBatteryLabel
from schemas.bodyBattery import BodyBattery


class BodyBatteryService:
    """
    Service class for managing body battery data including ingestion, retrieval,
    labeling, prediction storage, and DataFrame transformation.
    """

    __log = logging.getLogger(__name__)
    __repository = BodyBatteryRepository()
    __label_repository = BodyBatteryLabelsRepository()

    async def save_many(self, stressDetails):
        """
        Processes and saves body battery entries from stress detail input.

        Parameters:
        -----------
        stressDetails : StressDetails
            DTO containing stress details and timeOffsetBodyBatteryValues.

        Returns:
        --------
        StressDetails
            The original DTO after saving mapped entries.
        """
        if not stressDetails.stressDetails:
            return {}

        bodyBatteryEntries = []
        for stressDetail in stressDetails.stressDetails:
            for key, value in stressDetail.timeOffsetBodyBatteryValues.items():
                if int(key) % 900 == 0:  # Save every 15 minutes
                    bodyBatteryEntry = BodyBatteryMapper.from_stress_detail(stressDetail, key, value).to_json()
                    self.__log.debug(bodyBatteryEntry)
                    bodyBatteryEntries.append(bodyBatteryEntry)

        await self.__repository.save_many(sorted(bodyBatteryEntries, key=lambda e: e['timestamp']))
        return stressDetails

    async def find_many(self, userAccessToken: str, start: int, end: int):
        """
        Retrieves body battery entries within a specific time range.

        Parameters:
        -----------
        userAccessToken : str
            The user's access token.
        start : int
            Start timestamp (inclusive).
        end : int
            End timestamp (inclusive).

        Returns:
        --------
        List[BodyBattery]
            Parsed body battery entries in the specified time range.
        """
        if not start <= end:
            raise ValueError('timeStart must be before timeEnd!')

        result = await self.__repository.find_many(userAccessToken, start, end)
        entries = [BodyBattery.parse_obj(res) for res in result]
        return entries

    async def find_all(self, userId: str):
        """
        Retrieves all body battery entries for a given user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[BodyBattery]
            All stored body battery records for the user.
        """
        result = await self.__repository.find_all(userId)
        entries = [BodyBattery.parse_obj(res) for res in result]
        return entries

    async def find_all_to_dataframe(self, userId: str):
        """
        Retrieves all body battery entries for a user and converts them to a DataFrame.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        DataFrame
            A pandas DataFrame of all body battery records.
        """
        result = await self.find_all(userId)
        return BodyBatteryMapper.to_dataframe(data=result)

    async def label_body_battery(self, userId: str, labels: List[BodyBatteryLabel]):
        """
        Applies manual labels to the user's body battery data.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        labels : List[BodyBatteryLabel]
            A list of labels to update in the dataset.

        Returns:
        --------
        Any
            Result from the repository update operation.
        """
        return await self.__label_repository.update_many(userId, labels)

    async def reset_all_body_battery_labels(self, userId: str):
        """
        Removes all manual labels from a user's body battery records.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        Any
            Result from the repository reset operation.
        """
        return await self.__label_repository.reset_many(userId)

    async def add_body_battery_predictions(self, userId: str, labels: List[BodyBatteryLabel]):
        """
        Adds prediction labels to a user's body battery data.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        labels : List[BodyBatteryLabel]
            A list of predicted labels to update.

        Returns:
        --------
        Any
            Result from the repository update operation.
        """
        return await self.__label_repository.update_predictions(userId, labels)
