from adastra_library.adastra_library.unique_object import UniqueObject


class User(UniqueObject):
    """

    The most basic implementation of User.
    Only contains name and unique id
    """

    def __init__(self, name=None, unique_id=None):
        """

            :param name: {string} Name
            :param unique_id: {string} Unique id of object
                (use for restoring only )
        """
        super(User, self).__init__(name, unique_id)
