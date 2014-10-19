from xd.build.core.recipe_file import *

import unittest

class tests(unittest.case.TestCase):

    def test_split_no_version(self):
        name, version = RecipeFile.split_name_and_version('foo')
        self.assertEqual(name, 'foo')
        self.assertEqual(str(version), '')

    def test_split_version_1(self):
        name, version = RecipeFile.split_name_and_version('foo_4.2')
        self.assertEqual(name, 'foo')
        self.assertEqual(str(version), '4.2')

    def test_split_version_2(self):
        name, version = RecipeFile.split_name_and_version('foo_4.2.xd')
        self.assertEqual(name, 'foo')
        self.assertEqual(str(version), '4.2')

    def test_split_bad_version_1(self):
        with self.assertRaises(InvalidRecipeName):
            RecipeFile.split_name_and_version('')

    def test_split_bad_version_2(self):
        with self.assertRaises(InvalidRecipeName):
            RecipeFile.split_name_and_version('foo_bar_4.2')

    def test_with_path_1(self):
        recipe_file = RecipeFile('/path/to/something/foo.xd')
        self.assertEqual(recipe_file.name, 'foo')
        self.assertEqual(str(recipe_file.version), '')

    def test_with_path_2(self):
        recipe_file = RecipeFile('/some/path/bar_31.7.xd')
        self.assertEqual(recipe_file.name, 'bar')
        self.assertEqual(str(recipe_file.version), '31.7')

    def test_with_odd_path_1(self):
        with self.assertRaises(InvalidRecipeFilename):
            RecipeFile('/some/path/.xd')

    def test_bad_filename_1(self):
        with self.assertRaises(InvalidRecipeFilename):
            RecipeFile('/tmp/foo.bar')

    def test_bad_filename_2(self):
        with self.assertRaises(InvalidRecipeFilename):
            RecipeFile('/tmp/foo')

    def test_badd_filename_3(self):
        with self.assertRaises(InvalidRecipeFilename):
            RecipeFile('/some/path/.xd')

    def test_badd_filename_4(self):
        with self.assertRaises(InvalidRecipeFilename):
            RecipeFile('/some/path/foo_bar_1.xd')

    def test_with_odd_name(self):
        recipe_file = RecipeFile('/some/path/bar.93-1_4.xd')
        self.assertEqual(recipe_file.name, 'bar.93-1')
        self.assertEqual(str(recipe_file.version), '4')

    def test_with_odd_version_1(self):
        recipe_file = RecipeFile('/some/path/bar_4.2.1rc3.1-1.xd')
        self.assertEqual(recipe_file.name, 'bar')
        self.assertEqual(str(recipe_file.version), '4.2.1rc3.1-1')

    def test_with_odd_version_2(self):
        recipe_file = RecipeFile('/some/path/bar_89.23~build-189.xd')
        self.assertEqual(recipe_file.name, 'bar')
        self.assertEqual(str(recipe_file.version), '89.23~build-189')

    def test_str_1(self):
        recipe_file = RecipeFile('/tmp/foo.xd')
        self.assertEqual(str(recipe_file), 'foo')

    def test_str_2(self):
        recipe_file = RecipeFile('/tmp/foo_1.89.xd')
        self.assertEqual(str(recipe_file), 'foo_1.89')

    def test_repr(self):
        recipe_file = RecipeFile('/tmp/foo_1.89.xd')
        self.assertEqual(repr(recipe_file), "RecipeFile('/tmp/foo_1.89.xd')")

    def test_eq_1(self):
        recipe_file_a = RecipeFile('/tmp/foo_1.89.xd')
        recipe_file_b = RecipeFile('/tmp/foo_1.89.xd')
        self.assertEqual(recipe_file_a, recipe_file_b)

    def test_eq_2(self):
        recipe_file_a = RecipeFile('/tmp/foo_1.89.xd')
        recipe_file_b = RecipeFile('/tmp/foo_1.90.xd')
        self.assertNotEqual(recipe_file_a, recipe_file_b)

    def test_eq_3(self):
        recipe_file_a = RecipeFile('/tmp/foo_1.89.xd')
        recipe_file_b = '/tmp/foo_1.89.xd'
        self.assertNotEqual(recipe_file_a, recipe_file_b)
