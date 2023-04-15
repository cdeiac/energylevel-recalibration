import logging

import uvicorn
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Request
from fastapi.routing import APIRouter
from starlette.config import Config
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

from config.garmin import BASE_URL, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL, AUTH_URL
from config.mongodb import MongoDB
from routers.api import api
from routers.push import push
from routers.user import user
from routers.workflow import workflow

app = FastAPI()
mongodb = MongoDB()


config = Config('.env')
oauth = OAuth(config)
log = logging.getLogger(__name__)

app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(push)
app.include_router(api)
app.include_router(workflow)
app.include_router(user)
api_router = APIRouter()
oauth.register(name='garmin',
               api_base_url=BASE_URL,
               request_token_url=REQUEST_TOKEN_URL,
               access_token_url=ACCESS_TOKEN_URL,
               authorize_url=AUTH_URL,
               client_id=config.get('CLIENT_ID'),
               client_secret=config.get('CLIENT_SECRET'))


@app.on_event('startup')
async def on_startup():
    mongodb.init_mongodb()


@app.on_event('shutdown')
async def on_shutdown():
    mongodb.stop_mongodb()


@app.route('/')
async def entry(request: Request):
    # handle OAuth1 login and consent process in a single route due to available proxy mappings
    # currently, the user is tied to a session
    user = request.session.get('user')
    auth_initiated = False
    try:
        auth_initiated = request.session['auth_initiated']
    except KeyError:
        pass

    if user:
        # user is already logged in
        userId = user['userId']
        html = (
            f'<pre>Currently logged in as User: {userId}</pre>'
        )
        return HTMLResponse(html)
    elif auth_initiated:
        # fetch userId of logged in user
        token = await oauth.garmin.authorize_access_token(request)
        log.debug(token)
        request.session['token'] = dict(token)
        user_id_url = '/wellness-api/rest/user/id'
        resp = await oauth.garmin.get(user_id_url, token=token)
        user = resp.json()
        request.session['user'] = dict(user)
        return RedirectResponse(url='/')
    else:
        # login + consent
        #redirect_uri = request.url_for('auth')
        request.session['auth_initiated'] = True
        return await oauth.garmin.authorize_redirect(request)#, redirect_uri)


#@app.get('/wellness-api/stressDetails')
#async def get_stress_details(request: Request, startTime: str, endTime: str):
#    stressdetails_url = f'/wellness-api/rest/stressDetails?' \
#                        f'uploadStartTimeInSeconds={startTime}' \
#                        f'&uploadEndTimeInSeconds={endTime}'
#    response = await oauth.garmin.get(stressdetails_url, token=__get_session_token(request))
#    return Response(status_code=response.status_code)


def __get_session_token(request):
    token = request.session.get('token')
    return token


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000, log_level='debug', log_config='logging.yaml')
