import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *


__all__ = ['Bool', 'Int', 'Float']


class Bool(Variable):

    __slots__ = []

    basetype = bool


class Int(Variable):

    __slots__ = []

    basetype = int


class Float(Variable):

    __slots__ = []

    basetype = float
