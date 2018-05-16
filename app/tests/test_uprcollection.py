import unittest

from app.model.uprscollection import UPRSCollection


class TestUPRSCollection(unittest.TestCase):
    def setUp(self):
        self.uprs_collection = UPRSCollection()

    def tearDown(self):
        self.uprs_collection = None

    def test_uprs(self):
        self.assertListEqual(self.uprs_collection.uprs, [])

    def test_add_upr(self):
        upr = self.uprs_collection.add_upr("Any", "Any other")
        self.assertListEqual(self.uprs_collection.uprs, [upr])

    def test_remove_by_project_id(self):
        upr = self.uprs_collection.add_upr("any", "any other")
        self.uprs_collection.remove_by_project_id(upr.project_id)
        self.assertListEqual(self.uprs_collection.uprs, [])

    def test_remove_upr(self):
        upr = self.uprs_collection.add_upr("some", "any")
        upr2 = self.uprs_collection.add_upr("some other", "any other")
        self.uprs_collection.remove_upr(upr.user_id, upr.project_id)
        self.assertIn(upr2, self.uprs_collection.uprs)
        self.assertNotIn(upr, self.uprs_collection.uprs)
