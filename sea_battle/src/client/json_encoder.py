import json

from src.enums import condition


class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, condition):
            return obj.value
        return json.JSONEncoder.default(self, obj)
