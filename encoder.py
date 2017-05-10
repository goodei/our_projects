import json

from datetime import datetime,timezone


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%H:%M:%S %d.%m.%Y')
        return super().default(obj)


def decode(dct):
    for key,value in dct.items():
        try:
            dct[key] = datetime.strptime(value, '%H:%M:%S %d.%m.%Y').replace(tzinfo = timezone.utc)
        except:
            continue
    return dct