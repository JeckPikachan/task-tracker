import uuid


class UniqueObject:
    def __init__(self, name=None, unique_id=None):
        self.unique_id = str((unique_id is None and uuid.uuid4()) or uuid.UUID(unique_id))
        self.name = name
