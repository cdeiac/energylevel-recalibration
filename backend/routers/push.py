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
from services.StressLevelService import StressLevelService

push = APIRouter(tags=['Push'], prefix='/backend/push')
bodyBatteryService = BodyBatteryService()
stressLevelService = StressLevelService()
respirationService = RespirationService()
sleepService = SleepService()
activityService = ActivityService()


@push.post('/stressDetails')
async def stress_notifications(stressDetails: StressDetails):
    await bodyBatteryService.save_many(stressDetails)
    await stressLevelService.save_many(stressDetails)
    return Response(status_code=status.HTTP_200_OK)


@push.post('/respiration')
async def respiration_notifications(respirationDetails: RespirationDetails):
    await respirationService.save_many(respirationDetails)
    return Response(status_code=status.HTTP_200_OK)


@push.post('/sleep')
async def sleep_notification(sleeps: Sleeps):
    await sleepService.save_many(sleeps)
    return Response(status_code=status.HTTP_200_OK)


@push.post('/activities')
async def activities_notification(activities: Activities):
    await activityService.save_many(activities)
    return Response(status_code=status.HTTP_200_OK)


