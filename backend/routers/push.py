from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from dtos.Activity import Activities
from dtos.respirationdetail import RespirationDetails
from dtos.sleep import Sleeps
from dtos.stressdetail import StressDetails
from services.ActivityService import ActivityService
from services.BodyBatteryService import BodyBatteryService
from services.RespirationService import RespirationService
from services.SleepService import SleepService
from services.StressService import StressLevelService

push = APIRouter(tags=['Push'], prefix='/backend/push')
bodyBatteryService = BodyBatteryService()
stressLevelService = StressLevelService()
respirationService = RespirationService()
sleepService = SleepService()
activityService = ActivityService()


@push.post('/stressDetails')
async def stress_notifications(stressDetails: StressDetails):
    """
    Handles incoming stress data by saving it to BodyBattery and StressLevel services.

    Parameters:
    -----------
    stressDetails : StressDetails
        A DTO containing multiple stress records.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful processing.
    """
    await bodyBatteryService.save_many(stressDetails)
    await stressLevelService.save_many(stressDetails)
    return Response(status_code=status.HTTP_200_OK)


@push.post('/respiration')
async def respiration_notifications(respirationDetails: RespirationDetails):
    """
    Handles incoming respiration data and saves it to the Respiration service.

    Parameters:
    -----------
    respirationDetails : RespirationDetails
        A DTO containing multiple respiration records.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful processing.
    """
    await respirationService.save_many(respirationDetails)
    return Response(status_code=status.HTTP_200_OK)


@push.post('/sleep')
async def sleep_notification(sleeps: Sleeps):
    """
    Handles incoming sleep data and saves it to the Sleep service.

    Parameters:
    -----------
    sleeps : Sleeps
        A DTO containing multiple sleep records.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful processing.
    """
    await sleepService.save_many(sleeps)
    return Response(status_code=status.HTTP_200_OK)


@push.post('/activities')
async def activities_notification(activities: Activities):
    """
    Handles incoming activity data and saves it to the Activity service.

    Parameters:
    -----------
    activities : Activities
        A DTO containing multiple activity records.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful processing.
    """
    await activityService.save_many(activities)
    return Response(status_code=status.HTTP_200_OK)
