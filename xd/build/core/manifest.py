import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

from xd.build.core.recipe_file import *
import configparser
import os
import glob


__all__ = ['Manifest', 'Layer', 'NotABuildLayer', 'RecipeNotFound']


class NotABuildLayer(Exception):
    pass
class RecipeNotFound(Exception):
    pass


class Manifest(object):
    """XD-build manifest."""

    def __init__(self, tool_manifest):
        """XD-build manifest constructor.

        Arguments:
        tool_manifest -- XD-tool manifest instance (xd.tool.manifest.Manifest)
        """
        self.topdir = tool_manifest.topdir
        self.configfile = tool_manifest.configfile
        self.config = configparser.ConfigParser()
        self.config.read(self.configfile)
        self.layers = []
        self.recipe_files = {}
        for layer in tool_manifest.layers:
            try:
                layer = Layer(self, layer)
            except NotABuildLayer as e:
                continue
            self.layers.append(layer)
            layer.find_recipe_files()
            for recipe_file in layer.recipe_files.values():
                try:
                    recipe_files = self.recipe_files[recipe_file.name]
                except KeyError:
                    recipe_files = self.recipe_files[recipe_file.name] = []
                recipe_files.append(recipe_file)
        for recipe_files in self.recipe_files.values():
            recipe_files.sort(key=lambda r: r.version, reverse=True)

    def get_recipe(self, recipe):
        """Get XD-build recipe from manifest.

        This method can be given a relative or absolute path to a recipe or a
        name and optionally version number of a recipe, and will return a
        RecipeFile instance if recipe is found, and None otherwise.

        Examples:
        manifest.get_recipe('build/core/recipes/foo/foo_42.xd')
        manifest.get_recipe('/manifest/build/core/recipes/foo/foo_42.xd')
        manifest.get_recipe('foo')
        manifest.get_recipe('foo_42')

        Arguments:
        recipe -- filename path or recipe name
        """
        assert isinstance(recipe, str)
        if recipe.endswith('.xd'):
            log.debug('%s looks like a recipe file'%(recipe))
            return self.get_recipe_file_by_path(recipe)
        elif not '/' in recipe:
            log.debug('%s looks like a recipe name'%(recipe))
            return self.get_recipe_file_by_name(recipe)
        else:
            log.debug('recipe not found: %s', recipe)
            return None

    def get_recipe_file_by_path(self, path):
        """Get XD-build recipe from manifest.

        Specialized version of get_recipe(), this version must be given a
        relative or absolute path, but otherwise works the same way as
        get_recipe().

        Arguments:
        path -- relative or absolute path to recipe
        """
        for layer in self.layers:
            recipe_file = layer.get_recipe_file(path)
            if recipe_file is not None:
                return recipe_file
        log.debug('recipe file not found: %s', path)
        return None

    def get_recipe_file_by_name(self, name):
        """Get XD-build recipe from manifest.

        Specialized version of get_recipe(), this version must be given the
        name and optionally version number of a recipe in the manifest, but
        otherwise works the same way as get_recipe().

        Arguments:
        name -- name and optionally a version number (separated by '_')
        """
        name, version = RecipeFile.split_name_and_version(name)
        if not name in self.recipe_files:
            return None
        recipe_files = self.recipe_files[name]
        for recipe_file in recipe_files:
            if recipe_file.version == version:
                return recipe_file
        if not version:
            return recipe_files[0]
        return None


class Layer(object):
    """XD-build layer."""

    def __init__(self, manifest, tool_layer):
        """XD-build layer constructor.

        Arguments:
        manifest -- XD-build manifest instance
        tool_layer -- XD-tool layer instance
        """
        self.manifest = manifest
        self.submodule = tool_layer.submodule
        self.path = tool_layer.path
        self.commit = tool_layer.commit
        self.configfile = tool_layer.configfile
        config = configparser.ConfigParser()
        config.read(self.configfile)
        if not config.has_section('build'):
            raise NotABuildLayer(tool_layer)
        self.config = config['build']
        self.priority = tool_layer.priority()

    def find_recipe_files(self):
        """Find all recipes files in manifest.

        This method searches the XD-build manifest for recipe files according
        to the 'recipes' option in the 'build' section of the layers '.xd'
        file.
        """
        self.recipe_files = {}
        if not 'recipes' in self.config:
            log.debug('build layer without recipes: %s', self.submodule)
            return
        for recipes_glob in self.config.get('recipes').split():
            if os.path.isabs(recipes_glob):
                log.warning('ignoring absolute recipes glob in %s layer: %s',
                            self.submodule, recipes_glob)
                continue
            recipes_glob = os.path.join(self.path, recipes_glob)
            log.debug('globbing %s', recipes_glob)
            for recipe_path in glob.glob(recipes_glob):
                log.debug('found recipe %s', recipe_path)
                recipe_path = os.path.realpath(recipe_path)
                self.recipe_files[recipe_path] = RecipeFile(recipe_path)

    def get_recipe_file(self, path):
        """Get recipe file from layer.

        This method returns a RecipeFile instance if path is a recipe in this
        layer.
        """
        path = os.path.realpath(path)
        try:
            return self.recipe_files[path]
        except KeyError:
            return None
