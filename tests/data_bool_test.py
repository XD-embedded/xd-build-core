from xd.build.core.data.num import Bool

import unittest

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        s = Bool(True)
        self.assertTrue(s.get())

    def test_init_get_2(self):
        s = Bool(False)
        self.assertFalse(s.get())

    def test_init_get_3(self):
        s = Bool()
        self.assertIsNone(s.get())

    def test_str_1(self):
        s = Bool(True)
        self.assertEqual(str(s), 'True')

    def test_str_2(self):
        s = Bool(False)
        self.assertEqual(str(s), 'False')

    def test_str_3(self):
        s = Bool()
        self.assertEqual(str(s), '')

    def test_set_get(self):
        s = Bool(True)
        self.assertEqual(s.get(), True)
        s.set(False)
        self.assertEqual(s.get(), False)
