from typing import Optional

from fastapi import APIRouter, Header
from starlette import status
from starlette.responses import Response

from services.BackfillService import BackfillService

user = APIRouter(tags=['User'], prefix='/backend/user')
backfill_service = BackfillService()


@user.post('/register')
async def register_user(userToken: Optional[str] = Header(None),
                        userSecret: Optional[str] = Header(None)):
    """
    Registers a user by triggering backfill of historic data using their token and secret.

    Parameters:
    -----------
    userToken : Optional[str]
        Garmin API user token provided in the request header.
    userSecret : Optional[str]
        Garmin API user secret provided in the request header.

    Returns:
    --------
    Response
        HTTP 200 OK after initiating backfill request.
    """
    # Lookup userId for userToken (Garmin API), replace token in DB for the given user
    await backfill_service.get_historic_data(userToken, userSecret)
    return Response(status_code=status.HTTP_200_OK)


@user.post('/delete')
async def delete_user(userToken: str):
    """
    Deletes all data for the user associated with the given token.

    Parameters:
    -----------
    userToken : str
        The user's token used to identify and delete associated data.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful deletion request (currently a placeholder).
    """
    return Response(status_code=status.HTTP_200_OK)
