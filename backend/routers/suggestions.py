from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from services.BodyBatteryService import BodyBatteryService

user = APIRouter(tags=['Suggestions'], prefix='/backend/suggestions', )
bodyBatteryService = BodyBatteryService()


@user.post('/register')
async def register_user():
    return Response(status_code=status.HTTP_200_OK)

