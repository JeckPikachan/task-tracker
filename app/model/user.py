from app.model.UniqueObject import UniqueObject


class User(UniqueObject):
    def __init__(self, **kwargs):
        name = kwargs.get('name', None)
        super(User, self).__init__(name, kwargs.get('unique_id', None))
