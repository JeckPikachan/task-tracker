from adastra_library import Priority, Status

PUBLIC_ENUMS = {
    'Priority': Priority,
    'Status': Status
}


def serialize_enum(obj):
    if type(obj) in PUBLIC_ENUMS.values():
        return {"__enum__": str(obj)}


def deserialize_enum(d):
    if d is None:
        return None
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d
