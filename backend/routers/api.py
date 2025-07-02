from fastapi import APIRouter
from pydantic.schema import date
from starlette import status
from starlette.responses import Response

from config.datetimeEncoder import JsonResponse
from dtos.BodyBatteryLabel import BodyBatteryLabel, BodyBatteryLabels
from services.ActivityService import ActivityService
from services.BodyBatteryService import BodyBatteryService
from services.RespirationService import RespirationService
from services.SleepService import SleepService
from services.StepsService import StepsService
from services.StressService import StressLevelService

api = APIRouter(tags=['API'], prefix='/backend/api')
bodyBatteryService = BodyBatteryService()
stressLevelService = StressLevelService()
respirationService = RespirationService()
sleepService = SleepService()
activityService = ActivityService()
stepsService = StepsService()

# Body Battery

@api.get('/bodyBattery')
async def get_filtered_body_battery(userId: str, start: int, end: int):
    """
    Returns filtered BodyBattery records for a user between two timestamps.
    """
    result = await bodyBatteryService.find_many(userId, start, end)
    return JsonResponse(result)

@api.post('/bodyBattery/label')
async def label_body_battery(userId: str, labels: BodyBatteryLabels):
    """
    Applies labels to BodyBattery data for a given user.
    """
    await bodyBatteryService.label_body_battery(userId, labels.labels)
    return Response(status_code=status.HTTP_200_OK)

@api.post('/bodyBattery/labels/reset')
async def reset_all_body_battery_labels(userId: str):
    """
    Resets all labels in BodyBattery data for a given user.
    """
    await bodyBatteryService.reset_all_body_battery_labels(userId)
    return Response(status_code=status.HTTP_200_OK)

@api.get('/bodyBattery/all')
async def get_all_body_battery(userId: str):
    """
    Returns all BodyBattery records for a given user.
    """
    result = await bodyBatteryService.find_all(userId)
    return JsonResponse(result)


# Stress Level

@api.get('/stressLevel')
async def get_filtered_stress_levels(userId: str, start: int, end: int):
    """
    Returns filtered stress level data for a user between two timestamps.
    """
    result = await stressLevelService.find_many(userId, start, end)
    return JsonResponse(result)

@api.get('/stressLevel/all')
async def get_all_stress_levels(userId: str):
    """
    Returns all stress level data for a given user.
    """
    result = await stressLevelService.find_all(userId)
    return JsonResponse(result)


# Respiration

@api.get('/respiration')
async def get_filtered_respiration(userId: str, dateStart: date, dateEnd: date):
    """
    Returns filtered respiration records for a user between two dates.
    """
    result = await respirationService.find_many(userId, dateStart, dateEnd)
    return JsonResponse(result)

@api.get('/respiration/all')
async def get_all_respiration(userId: str):
    """
    Returns all respiration records for a given user.
    """
    result = await respirationService.find_all(userId)
    return JsonResponse(result)


# Sleep

@api.get('/sleep')
async def get_filtered_sleep(userId: str, start: int, end: int):
    """
    Returns filtered sleep records for a user between two timestamps.
    """
    result = await sleepService.find_many(userId, start, end)
    return JsonResponse(result)

@api.get('/sleep/all')
async def get_all_sleep(userId: str):
    """
    Returns all sleep records for a given user.
    """
    result = await sleepService.find_all(userId)
    return JsonResponse(result)

@api.get('/sleep/statistics/all')
async def get_all_sleep_statistics(userId: str):
    """
    Returns all sleep statistics for a given user.
    """
    result = await sleepService.find_all_statistics(userId)
    return JsonResponse(result)

@api.get('/sleep/statistics')
async def get_all_sleep_statistics(userId: str, start: int, end: int):
    """
    Returns filtered sleep statistics for a user between two timestamps.
    """
    result = await sleepService.find_many_statistics(userId, start, end)
    return JsonResponse(result)

@api.get('/sleep/statistics/date')
async def get_all_sleep_statistics_for_date(userId: str, targetDate: date):
    """
    Returns sleep statistics for a user for a specific date.
    """
    result = await sleepService.find_one_statistic(userId, targetDate)
    return JsonResponse(result)

@api.get('/sleep/statistics/awake-time')
async def get_awake_time(userId: str, targetDate: date):
    """
    Returns total awake time for a user on a specific date.
    """
    result = await sleepService.find_awake_time(userId, targetDate)
    return JsonResponse(result)


# Activities

@api.get('/activities')
async def get_filtered_stress_levels(userId: str, start: int, end: int):
    """
    Returns filtered activity records for a user between two timestamps.
    """
    result = await activityService.find_many(userId, start, end)
    return JsonResponse(result)

@api.get('/activities/all')
async def get_all_activities(userId: str):
    """
    Returns all activity records for a given user.
    """
    result = await activityService.find_all(userId)
    return JsonResponse(result)


# Steps

@api.get('/steps/all')
async def get_all_steps(userId: str):
    """
    Returns all step records for a given user.
    """
    result = await stepsService.find_all(userId)
    return JsonResponse(result)
