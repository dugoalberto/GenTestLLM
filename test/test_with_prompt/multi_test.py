import unittest
from unittest import TestCase

from classes.Desk import Desk
from classes.Office import Office


class TestOffice(TestCase):
    def test_maximum_desks(self):
        desk1 = Desk(100, 100, 100)
        office = Office("Via Roma 1", 100, [desk1])
        self.assertEqual(office.maximum_desks(), 100)
    def test_desks_quantity(self):
        desk1 = Desk(100, 100, 100)
        desk2 = Desk(100, 100, 100)
        desk3 = Desk(100, 100, 100)
        office = Office("Via Roma 1", 1000, [desk1, desk2, desk3])
        self.assertEqual(office.desks_quantity(), 3)
    def test_get_address(self):
        office = Office("Via Roma 1", 1000, [])
        self.assertEqual(office.get_address(), "Via Roma 1")
