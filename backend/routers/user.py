from typing import Optional

from fastapi import APIRouter, Header
from starlette import status
from starlette.responses import Response

from services.BackfillService import BackfillService

user = APIRouter(tags=['User'], prefix='/backend/user', )
backfill_service = BackfillService()


@user.post('/register')
async def register_user(userToken: Optional[str] = Header(None),
                        userSecret: Optional[str] = Header(None)):
    #lookup userId for userToken (garmin api), replace token in DB for the given user
    await backfill_service.get_historic_data(userToken, userSecret)
    return Response(status_code=status.HTTP_200_OK)


@user.post('/delete')
async def delete_user(userToken: str):
    """
        Deletes all data for the user associated with the given token
    """
    return Response(status_code=status.HTTP_200_OK)

