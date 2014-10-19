import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


import distutils.version


__all__ = ['RecipeVersion']


class RecipeVersion(distutils.version.LooseVersion):
    """Version number for XD-build recipes.

    To be able to allow the recipe version number to match the version number
    of the software project the recipe integrates, any string is considered a
    valid version number.

    Anything else than simple multi-digit version numbers (like 1.3 and 4.7.2)
    might not compare (as in less than and greater than operations) as
    expected.
    """

    def __init__(self, vstring=''):
        """Create a new version number.

        Arguments:
        vstring -- version number string
        """
        self.parse(vstring)

    def parse(self, vstring):
        """Parse and set a (new) version number.

        Arguments:
        vstring -- version number string
        """
        super(RecipeVersion, self).parse(vstring)

    def __str__(self):
        return self.vstring or ''

    def __repr__(self):
        return '%s (%r)'%(self.__class__.__name__, self.vstring)

    def __bool__(self):
        return bool(self.vstring)
