from xd.build.core.recipe_version import *

import unittest

class tests(unittest.case.TestCase):

    def test_single_digit(self):
        version = RecipeVersion('1')
        self.assertEqual(str(version), '1')

    def test_double_digit(self):
        version = RecipeVersion('2.3')
        self.assertEqual(str(version), '2.3')

    def test_triple_digit(self):
        version = RecipeVersion('4.5.6')
        self.assertEqual(str(version), '4.5.6')

    def test_default_constructor(self):
        version = RecipeVersion()
        self.assertEqual(str(version), '')

    def test_empty_string(self):
        version = RecipeVersion('')
        self.assertEqual(str(version), '')

    def test_bool_false(self):
        self.assertEqual(bool(RecipeVersion()), False)

    def test_bool_true(self):
        self.assertEqual(bool(RecipeVersion('7.8')), True)

    def test_equal(self):
        v1a = RecipeVersion('1.2')
        v1b = RecipeVersion('1.2')
        v2 = RecipeVersion('3.4')
        self.assertEqual(v1a, v1b)
        self.assertNotEqual(v1a, v2)
        self.assertNotEqual(v1b, v2)

    def test_less_and_greater_than(self):
        v1 = RecipeVersion('1')
        v12 = RecipeVersion('1.2')
        v2 = RecipeVersion('2')
        v34 = RecipeVersion('3.4')
        self.assertLess(v1, v12)
        self.assertLess(v1, v2)
        self.assertLess(v1, v34)
        self.assertLess(v12, v2)
        self.assertLess(v12, v34)
        self.assertLess(v2, v34)
        self.assertGreater(v34, v2)
        self.assertGreater(v34, v12)
        self.assertGreater(v34, v1)
        self.assertGreater(v2, v12)
        self.assertGreater(v2, v1)
        self.assertGreater(v12, v1)

    def test_repr(self):
        v1 = RecipeVersion('1.2')
        v1_repr = repr(v1)
        v2 = eval(v1_repr)
        self.assertEqual(v1, v2)
