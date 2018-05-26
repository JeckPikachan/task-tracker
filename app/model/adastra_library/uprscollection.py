from app.model.adastra_library.userprojectrelation import UserProjectRelation


class UPRSCollection:
    def __init__(self, uprs=None):
        """

        :param uprs: {UserProjectRelation[]} list of UserProjectRelation objects
        """
        self.uprs = [UserProjectRelation(**upr) for upr in uprs] if\
            uprs is not None else []

    def add_upr(self, user_id, project_id):
        """
        Creates and adds UserProjectRelation object with
        specified user id and project id.

        :param user_id: {string} User id of UPR to be added
        :param project_id: {string} Project id of UPR to be added
        :return: Created UserProjectRelation object
        """
        new_upr = UserProjectRelation(user_id, project_id)
        self.uprs.append(new_upr)
        return new_upr

    def remove_by_project_id(self, project_id):
        """
        Removes all UserProjectRelation object with specified project id

        :param project_id: {string} Project id
        """
        self.uprs = [upr for upr in self.uprs if upr.project_id != project_id]

    def remove_upr(self, user_id, project_id):
        """
        Removes UserProjectRelation with specified user id and
        project id

        :param user_id: {string} User id of UPR to be removed
        :param project_id: {string} Project id of UPR to be removed
        """
        self.uprs = [upr for upr in self.uprs if
                     upr.project_id != project_id or upr.user_id != user_id]
