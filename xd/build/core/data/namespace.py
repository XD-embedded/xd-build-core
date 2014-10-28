import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__all__ = ['Namespace']


class Namespace(dict):
    """XD-build data namespaces.

    Class for holding a namespace of XD-build data variables.  It is
    implemented as a mapping so it can be used as a locals to eval().
    """
    pass
