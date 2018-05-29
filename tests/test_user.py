import unittest

from adastra_library.adastra_library.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def tearDown(self):
        self.user = None

    def test_name(self):
        self.assertIsNone(self.user.name)

    def test_unique_id(self):
        self.assertIsInstance(self.user.unique_id, str)
