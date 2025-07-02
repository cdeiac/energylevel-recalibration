from datetime import datetime

import pytz
from fastapi.encoders import jsonable_encoder


def JsonResponse(obj):
    """
        Encodes a given Python object into a JSON-serializable format, ensuring that
        all datetime objects are converted to UTC timezone.

        Parameters:
        obj (Any): The Python object to be encoded, which may contain datetime instances.

        Returns:
        Any: A JSON-serializable representation of the input object, with all datetime
             objects converted to UTC timezone.
    """
    return jsonable_encoder(obj, custom_encoder={datetime: lambda date_obj: date_obj.astimezone(pytz.utc)})
