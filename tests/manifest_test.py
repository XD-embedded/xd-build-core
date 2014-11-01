from xd.build.core.manifest import *

from case import *

class tests(ManifestTestCase):

    def test_init(self):
        manifest = Manifest(self.manifest)
        self.assertEqual(len(manifest.layers), 1)
        self.assertEqual(len(manifest.layers[0].recipe_files), 2)
        self.assertIn(os.path.join(self.layerdir, 'recipes', 'foo_1.0.xd'),
                      manifest.layers[0].recipe_files)
        self.assertIn(os.path.join(self.layerdir, 'recipes', 'bar.xd'),
                      manifest.layers[0].recipe_files)

    def test_init_not_a_build_layer(self):
        configfile = self.manifest.layers[0].configfile
        os.unlink(configfile)
        with open(configfile, 'w') as f:
            pass
        manifest = Manifest(self.manifest)
        self.assertEqual(len(manifest.layers), 0)

    def test_init_without_recipes(self):
        configfile = self.manifest.layers[0].configfile
        config = configparser.ConfigParser()
        config.read(configfile)
        config.remove_option('build', 'recipes')
        with open(configfile, 'w') as f:
            config.write(f)
        manifest = Manifest(self.manifest)
        self.assertEqual(len(manifest.layers[0].recipe_files), 0)

    def test_init_with_absolute_recipes_glob(self):
        configfile = self.manifest.layers[0].configfile
        config = configparser.ConfigParser()
        config.read(configfile)
        config['build']['recipes'] = '/recipes/*.xd'
        with open(configfile, 'w') as f:
            config.write(f)
        manifest = Manifest(self.manifest)
        self.assertEqual(len(manifest.layers[0].recipe_files), 0)

    def test_get_recipe_name_found_1a(self):
        manifest = Manifest(self.manifest)
        self.assertTrue(manifest.get_recipe('foo'))

    def test_get_recipe_name_found_1b(self):
        manifest = Manifest(self.manifest)
        self.assertTrue(manifest.get_recipe('foo_1.0'))

    def test_get_recipe_name_found_2(self):
        manifest = Manifest(self.manifest)
        self.assertTrue(manifest.get_recipe('bar'))

    def test_get_recipe_name_not_found_1(self):
        manifest = Manifest(self.manifest)
        self.assertIsNone(manifest.get_recipe('foobar'))

    def test_get_recipe_name_not_found_2(self):
        manifest = Manifest(self.manifest)
        self.assertIsNone(manifest.get_recipe('bar_0'))

    def test_get_recipe_absolute_path_found(self):
        manifest = Manifest(self.manifest)
        self.assertTrue(manifest.get_recipe(
            os.path.join(self.layerdir, 'recipes', 'bar.xd')))

    def test_get_recipe_absolute_path_not_found(self):
        manifest = Manifest(self.manifest)
        self.assertIsNone(manifest.get_recipe(
            os.path.join(self.layerdir, 'recipes', 'foo.xd')))

    def test_get_recipe_bad_path(self):
        manifest = Manifest(self.manifest)
        self.assertIsNone(manifest.get_recipe(
            os.path.join(self.layerdir, 'recipes', 'bar')))
