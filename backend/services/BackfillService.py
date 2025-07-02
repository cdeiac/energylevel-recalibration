import requests
from starlette.config import Config
from requests_oauthlib import OAuth1

config = Config('.env')

class BackfillService:
    """
    Service responsible for fetching historic data from the Garmin Health API
    using OAuth1 authentication and predefined start/end timestamps.
    """

    BASE_URL = config.get('GARMIN_HEALTH_API_HOST')

    async def get_historic_data(self, userToken: str, userSecret: str):
        """
        Fetches historic respiration data for a user using their OAuth credentials.

        Parameters:
        -----------
        userToken : str
            OAuth token for the user.
        userSecret : str
            OAuth secret for the user.

        Returns:
        --------
        None
        """
        url = self.BASE_URL + '/respiration'
        auth = OAuth1(
            config.get('CLIENT_ID'),
            config.get('CLIENT_SECRET'),
            userToken,
            userSecret
        )
        response_code = requests.get(
            url,
            params={
                "uploadStartTimeInSeconds": 1568165927,
                "uploadEndTimeInSeconds": 1568245127
            },
            auth=auth
        )

        print('Completed Request: ' + str(response_code))
