from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from services.BodyBatteryService import BodyBatteryService

user = APIRouter(tags=['Suggestions'], prefix='/backend/suggestions')
bodyBatteryService = BodyBatteryService()


@user.post('/register')
async def register_user():
    """
    Placeholder endpoint for registering a user for suggestion services.

    Returns:
    --------
    Response
        HTTP 200 OK indicating the request was successfully received.
    """
    return Response(status_code=status.HTTP_200_OK)
