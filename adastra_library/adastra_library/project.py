from .UniqueObject import UniqueObject


class Project(UniqueObject):
    """

    Project is biggest building block of Task Tracker
    Task lists and tasks exist in terms of project only
    """

    def __init__(self, **kwargs):
        """

        :param kwargs: can include:
            name: {string} Name of project
            unique_id: {string} Sets unique id of task
                (use for restoring only)
            lists: {string[]} List of included task ids
        """
        name = kwargs.get('name')
        super(Project, self).__init__(name, kwargs.get('unique_id', None))
        self.lists = kwargs.get('lists', [])
        self.roles_list = kwargs.get('roles_list', [])
