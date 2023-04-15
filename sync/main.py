import uvicorn
import json

from fastapi import FastAPI, Body
from starlette import status
from starlette.responses import Response

app = FastAPI()


@app.post('/')
async def entry(payload: dict = Body(...)):
    with open('data.json', 'a') as fp:
        json.dump(payload, fp, indent=2)
        fp.write('\n')
    return payload
    #return Response(status_code=status.HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=3000)
