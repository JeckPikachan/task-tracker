from app.model.userprojectrelation import UserProjectRelation


class UPRSCollection:
    def __init__(self, uprs=None):
        self.uprs = [UserProjectRelation(**upr) for upr in uprs] if uprs is not None else []

    def add_upr(self, user_id, project_id):
        new_upr = UserProjectRelation(user_id, project_id)
        self.uprs.append(new_upr)
        return new_upr

    def remove_by_project_id(self, project_id):
        self.uprs = [upr for upr in self.uprs if upr.project_id != project_id]

    def remove_upr(self, user_id, project_id):
        self.uprs = [upr for upr in self.uprs if
                     upr.project_id != project_id or upr.user_id != user_id]