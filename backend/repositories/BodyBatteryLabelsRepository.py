from typing import List
from pydantic.schema import datetime
from pymongo import ReturnDocument

from config.mongodb import MongoDB
from schemas.BodyBatteryLabel import BodyBatteryLabel


class BodyBatteryLabelsRepository:
    """
    Repository for performing CRUD operations on the 'bodyBattery' collection,
    specifically for managing BodyBattery labels and predictions.
    """

    # target DB
    mongoDb = MongoDB()
    __bodyBatteryLabelsDB = mongoDb.db['bodyBattery']

    async def save(self, bodyBatteryLabel: BodyBatteryLabel):
        """
        Inserts a single BodyBatteryLabel document into the database.

        Parameters:
        -----------
        bodyBatteryLabel : BodyBatteryLabel
            The label document to be saved.

        Returns:
        --------
        InsertOneResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not bodyBatteryLabel:
            return {}

        return await self.__bodyBatteryLabelsDB.insert_one(bodyBatteryLabel)

    async def save_many(self, userId: str, bodyBatteryLabels: List[BodyBatteryLabel]):
        """
        Inserts multiple BodyBatteryLabel documents into the database.

        Parameters:
        -----------
        userId : str
            The user ID associated with the labels.
        bodyBatteryLabels : List[BodyBatteryLabel]
            A list of labels to insert.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not bodyBatteryLabels:
            return {}
        # TODO: Upsert
        return self.__bodyBatteryLabelsDB.insert_many(userId, bodyBatteryLabels)

    async def update_many(self, userId: str, labels: List[BodyBatteryLabel]):
        """
        Updates the 'label' field of multiple documents for a given user.

        Parameters:
        -----------
        userId : str
            The user ID to filter documents.
        labels : List[BodyBatteryLabel]
            A list of label updates to apply.

        Returns:
        --------
        None
        """
        if not labels:
            return {}

        for label in labels:
            self.__bodyBatteryLabelsDB.update_one(
                {'userId': userId, 'timestamp': int(label.timestamp)},
                {'$set': {'label': int(label.label)}}
            )

    async def reset_many(self, userId: str):
        """
        Removes the 'label' field from all documents for the specified user.

        Parameters:
        -----------
        userId : str
            The user ID whose labels should be reset.

        Returns:
        --------
        None
        """
        self.__bodyBatteryLabelsDB.update_many(
            {'userId': userId},
            {'$unset': {'label': ''}}
        )

    async def update_predictions(self, userId: str, labels: List[BodyBatteryLabel]):
        """
        Updates the 'prediction' field for multiple documents.

        Parameters:
        -----------
        userId : str
            The user ID to filter documents.
        labels : List[BodyBatteryLabel]
            A list of prediction updates to apply.

        Returns:
        --------
        None or dict
            An empty dict if input is invalid.
        """
        if not labels:
            return {}

        for label in labels:
            self.__bodyBatteryLabelsDB.update_one(
                {'userId': userId, 'timestamp': int(label.timestamp)},
                {'$set': {'prediction': int(label.label)}}
            )

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        """
        Retrieves all BodyBatteryLabel documents within a time range for a user.

        Parameters:
        -----------
        userId : str
            The user ID to filter documents.
        timeStart : datetime
            Start of the time range (inclusive).
        timeEnd : datetime
            End of the time range (exclusive).

        Returns:
        --------
        List[dict]
            A list of matching documents.
        """
        cursor = self.__bodyBatteryLabelsDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': timeStart,
                    '$lt': timeEnd
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str):
        """
        Retrieves all BodyBatteryLabel documents for a user.

        Parameters:
        -----------
        userId : str
            The user ID to filter documents.

        Returns:
        --------
        List[dict]
            A list of all documents for the specified user.
        """
        cursor = self.__bodyBatteryLabelsDB.find({'userId': userId})
        return [doc async for doc in cursor]
