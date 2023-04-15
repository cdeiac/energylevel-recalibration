from datetime import datetime
from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from config.datetimeEncoder import JsonResponse
from dtos.BodyBatteryLabel import BodyBatteryLabel
from services.ActivityService import ActivityService
from services.BodyBatteryService import BodyBatteryService
from services.RespirationService import RespirationService
from services.SleepService import SleepService
from services.StepsService import StepsService
from services.StressLevelService import StressLevelService

api = APIRouter(tags=['API'], prefix='/backend/api')
bodyBatteryService = BodyBatteryService()
stressLevelService = StressLevelService()
respirationService = RespirationService()
sleepService = SleepService()
activityService = ActivityService()
stepsService = StepsService()

# Body Battery

@api.get('/bodyBattery')
async def get_filtered_body_battery(userId: str, timeStart: datetime, timeEnd: datetime):
    result = await bodyBatteryService.find_many(userId, timeStart, timeEnd)
    return JsonResponse(result)

@api.post('/bodyBattery/label')
async def label_body_battery(userId: str, labels: List[BodyBatteryLabel]):
    await bodyBatteryService.label_body_battery(userId, labels)
    return Response(status_code=status.HTTP_200_OK)


@api.get('/bodyBattery/all')
async def get_all_body_battery(userId: str):
    result = await bodyBatteryService.find_all(userId)
    return JsonResponse(result)


# Stress Level

@api.get('/stressLevel')
async def get_filtered_stress_levels(userId: str, timeStart: datetime, timeEnd: datetime):
    result = await stressLevelService.find_many(userId, timeStart, timeEnd)
    return JsonResponse(result)

@api.get('/stressLevel/all')
async def get_all_stress_levels(userId: str):
    result = await stressLevelService.find_all(userId)
    return JsonResponse(result)


# Respiration

@api.get('/respiration')
async def get_filtered_respiration(userId: str, timeStart: datetime, timeEnd: datetime):
    result = await respirationService.find_many(userId, timeStart, timeEnd)
    return JsonResponse(result)

@api.get('/respiration/all')
async def get_all_respiration(userId: str):
    result = await respirationService.find_all(userId)
    return JsonResponse(result)


# Sleep

@api.get('/sleep')
async def get_filtered_sleep(userId: str, timeStart: datetime, timeEnd: datetime):
    result = await sleepService.find_many(userId, timeStart, timeEnd)
    return JsonResponse(result)

@api.get('/sleep/all')
async def get_all_sleep(userId: str):
    result = await sleepService.find_all(userId)
    return JsonResponse(result)

@api.get('/sleep/statistics/all')
async def get_all_sleep(userId: str):
    result = await sleepService.find_all_statistics(userId)
    return JsonResponse(result)


# Activities

@api.get('/activities')
async def get_filtered_stress_levels(userId: str, timeStart: datetime, timeEnd: datetime):
    result = await activityService.find_many(userId, timeStart, timeEnd)
    return JsonResponse(result)

@api.get('/activities/all')
async def get_all_activities(userId: str):
    result = await activityService.find_all(userId)
    return JsonResponse(result)


# Steps

@api.get('/steps/all')
async def get_all_steps(userId: str):
    result = await stepsService.find_all(userId)
    return JsonResponse(result)
