import unittest

from app.model.adastra_library.project import Project

NAME = "Some Name"


class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project(name=NAME)

    def tearDown(self):
        self.project = None

    def test_name(self):
        self.assertEqual(self.project.name, NAME)

    def test_unique_id_type(self):
        self.assertIsInstance(self.project.unique_id, str)

    def test_lists(self):
        self.assertListEqual(self.project.lists, [])

    def test_roles_list(self):
        self.assertListEqual(self.project.roles_list, [])
