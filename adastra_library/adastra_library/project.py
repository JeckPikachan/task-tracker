from adastra_library.adastra_library.unique_object import UniqueObject


class Project(UniqueObject):
    """

    Project is biggest building block of Task Tracker
    Task lists and tasks exist in terms of project only
    """

    def __init__(self, name=None, unique_id=None, lists=None, roles_list=None):
        """

        :param name: {string} Name of project
        :param unique_id: {string} Sets unique id of task
                (use for restoring only)
        :param lists: {string[]} List of included task ids
        :param roles_list: not implemented
        """
        super(Project, self).__init__(name, unique_id)
        self.lists = lists if lists is not None else []
        self.roles_list = roles_list if roles_list is not None else []
