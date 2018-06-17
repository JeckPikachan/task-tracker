import uuid


class UniqueObject:
    def __init__(self, name=None, unique_id=None):
        """

        :param name: {string} Name
        :param unique_id: {string} Unique id of object
            (use for restoring only )
        """
        self.unique_id = str((unique_id is None and uuid.uuid4()) or unique_id)
        self.name = name
