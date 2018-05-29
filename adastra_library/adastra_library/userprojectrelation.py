class UserProjectRelation:
    """
    Relation that unites user and project.
    You can think about it like edges of graph
    between users and projects.
    """
    def __init__(self, user_id, project_id, user_role=None):
        """

        :param user_id: {string} Id of user
        :param project_id: {string} Id of project
        :param user_role: Not implemented yet
        """
        self.user_id = user_id
        self.project_id = project_id
        self.user_role = None  # will be implemented later
