from dtw import *

from services.BodyBatteryService import BodyBatteryService


class SimilaritySearchService:
    """
    Service that computes time series similarity using Dynamic Time Warping (DTW)
    on body battery values to find historical days most similar to a target date.
    """

    __body_battery_service = BodyBatteryService()

    async def compute_distance(self, userId, target_date):
        """
        Finds the 10 most similar past days to a given date based on body battery values.

        Parameters:
        -----------
        userId : str
            The ID of the user whose data is being analyzed.
        target_date : str
            The calendar date to compare against (in YYYY-MM-DD format).

        Returns:
        --------
        List[str]
            A list of up to 10 calendar dates most similar to the target date, ordered by similarity.
        """
        # Gather all data and sort by timestamp
        list_of_bb = await self.__body_battery_service.find_all(userId)
        list_of_bb.sort(key=lambda x: x.timestamp, reverse=False)

        # Extract the target series and remove it from comparison
        target_series = [bb.value for bb in list_of_bb if bb.calendarDate == target_date]
        subject_series = [bb for bb in list_of_bb if bb.calendarDate != target_date]

        # Group values by calendarDate
        bb_dict = dict()
        for bb in subject_series:
            if bb.calendarDate not in bb_dict:
                bb_dict[bb.calendarDate] = [bb.value]
            else:
                bb_dict[bb.calendarDate].append(bb.value)

        distance_by_date = dict()
        # Compute DTW distances
        for date, series in bb_dict.items():
            distance = dtw(series, target_series)
            distance_by_date[date] = distance.distance

        # Sort and return 10 most similar dates
        sorted_distances = dict(sorted(distance_by_date.items(), key=lambda item: item[1]))
        return list(sorted_distances.keys())[:10]
