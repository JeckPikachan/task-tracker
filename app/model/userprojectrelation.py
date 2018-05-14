class UserProjectRelation:
    def __init__(self, user_id, project_id, user_role=None):
        self.user_id = user_id
        self.project_id = project_id
        self.user_role = None  # will be implemented later
