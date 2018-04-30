from model.UniqueObject import UniqueObject


class Project(UniqueObject):
    def __init__(self, **kwargs):
        name = kwargs.get('name')
        super(Project, self).__init__(name, kwargs.get('unique_id', None))
        self.lists = kwargs.get('lists', [])
        self.roles_list = kwargs.get('roles_list', [])
        self.user_project_relations_list = kwargs.get('user_project_relations_list', [])

