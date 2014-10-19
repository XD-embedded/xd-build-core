import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from xd.build.core.recipe_version import *
import os


__all__ = ['RecipeFile', 'InvalidRecipeName', 'InvalidRecipeFilename']


class InvalidRecipeName(Exception):
    pass
class InvalidRecipeFilename(Exception):
    pass


class RecipeFile(object):
    """XD-build recipe file.

    Instances of this class represents a single XD-build recipe file.
    """

    def __init__(self, path):
        """Recipe file constructor.

        Arguments:
        path -- filename path of recipe file (must end with '.xd')
        """
        if not path.endswith('.xd'):
            raise InvalidRecipeFilename(path)
        self.path = path
        try:
            self.name, self.version = self.split_name_and_version(self.path)
        except InvalidRecipeName:
            raise InvalidRecipeFilename(path)

    @classmethod
    def split_name_and_version(cls, filename):
        """Convert recipe filename to recipe name and version number.

        Arguments:
        filename -- recipe name or filename

        Returns:
        (name, version)
        name -- recipe name (str)
        version -- recipe version (RecipeVersion instance)
        """
        if filename.endswith('.xd'):
            filename = filename[:-3]
        filename = os.path.basename(filename)
        name_and_version = filename.split('_')
        if len(name_and_version) < 1 or len(name_and_version) > 2:
            raise InvalidRecipeName(filename)
        if len(name_and_version[0]) == 0:
            raise InvalidRecipeName(filename)
        name = name_and_version[0]
        try:
            version = name_and_version[1]
        except IndexError:
            version = ''
        version = RecipeVersion(version)
        return (name, version)

    def __str__(self):
        if self.version:
            return '%s_%s'%(self.name, self.version)
        else:
            return self.name

    def __repr__(self):
        return 'RecipeFile(%r)'%(self.path)

    def __eq__(self, other):
        if not isinstance(other, RecipeFile):
            return False
        if os.path.realpath(self.path) != os.path.realpath(other.path):
            return False
        return True
