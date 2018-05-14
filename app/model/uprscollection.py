from app.model.userprojectrelation import UserProjectRelation


class UPRSCollection:
    def __init__(self, uprs=None):
        self.uprs = [UserProjectRelation(**upr) for upr in uprs] if uprs is not None else []

    def add_upr(self, user_id, project_id):
        new_upr = UserProjectRelation(user_id, project_id)
        self.uprs.append(new_upr)
