from datetime import datetime

import pytz
from fastapi.encoders import jsonable_encoder


def JsonResponse(obj):
    return jsonable_encoder(obj, custom_encoder={datetime: lambda date_obj: date_obj.astimezone(pytz.utc)})
