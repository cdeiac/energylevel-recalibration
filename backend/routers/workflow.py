from datetime import date

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from dtos.stressdetail import StressDetails
from services.BodyBatteryService import BodyBatteryService
from services.WorkflowService import WorkflowService

workflow = APIRouter(tags=['Workflow'], prefix='/backend/workflow', )
bodyBatteryService = BodyBatteryService()
workflowService = WorkflowService()

@workflow.post('/query')
async def query(stressDetails: StressDetails):
    return Response(status_code=status.HTTP_200_OK)


@workflow.get('/init') # will not be exposed later, shall be triggered at login
async def train(userId: str):
    await workflowService.get_all_data(userId)
    return Response(status_code=status.HTTP_200_OK)


@workflow.post('/train')
async def train(stressDetails: StressDetails):
    return Response(status_code=status.HTTP_200_OK)


@workflow.post('/similarity-search')
async def similarity_search(userId: str, search_type: str, timeMin: date, timeMax: date):
    return Response(status_code=status.HTTP_200_OK)
