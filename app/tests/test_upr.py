import unittest

from app.model.adastra_library.userprojectrelation import UserProjectRelation

USER_ID = "SOME ID NO MATTER WHAT"
PROJECT_ID = "ANY OTHER OR NOT ID"


class TestUPR(unittest.TestCase):
    def setUp(self):
        self.upr = UserProjectRelation(USER_ID, PROJECT_ID)

    def tearDown(self):
        self.upr = None

    def test_user_id(self):
        self.assertEqual(self.upr.user_id, USER_ID)

    def test_project_id(self):
        self.assertEqual(self.upr.project_id, PROJECT_ID)
