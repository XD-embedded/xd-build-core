from xd.build.core.data.num import Float

import unittest

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        s = Float(3.14)
        self.assertEqual(s.get(), 3.14)

    def test_init_get_2(self):
        s = Float()
        self.assertIsNone(s.get())

    def test_str_1(self):
        s = Float(3.14)
        self.assertEqual(str(s), '3.14')

    def test_str_2(self):
        s = Float()
        self.assertEqual(str(s), '')

    def test_set_get(self):
        s = Float(3.14)
        self.assertEqual(s.get(), 3.14)
        s.set(22.7)
        self.assertEqual(s.get(), 22.7)
