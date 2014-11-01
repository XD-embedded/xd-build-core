from xd.build.core.data.num import Int

import unittest

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        s = Int(42)
        self.assertEqual(s.get(), 42)

    def test_init_get_2(self):
        s = Int()
        self.assertIsNone(s.get())

    def test_str_1(self):
        s = Int(42)
        self.assertEqual(str(s), '42')

    def test_str_2(self):
        s = Int()
        self.assertEqual(str(s), '')

    def test_set_get(self):
        s = Int(42)
        self.assertEqual(s.get(), 42)
        s.set(43)
        self.assertEqual(s.get(), 43)
