import json

from app.util.priority import Priority
from app.util.status import Status

PUBLIC_ENUMS = {
    'Priority': Priority,
    'Status': Status
}


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        enum_serializable(obj)
        return json.JSONEncoder.default(self, obj)


def enum_serializable(obj):
    if type(obj) in PUBLIC_ENUMS.values():
        return {"__enum__": str(obj)}


def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d
