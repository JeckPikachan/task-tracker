from app.model.UniqueObject import UniqueObject


class User(UniqueObject):
    """

    The most basic implementation of User.
    Only contains name and unique id
    """

    def __init__(self, **kwargs):
        """

            :param name: {string} Name
            :param unique_id: {string} Unique id of object
                (use for restoring only )
        """
        name = kwargs.get('name', None)
        super(User, self).__init__(name, kwargs.get('unique_id', None))
