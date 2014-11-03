import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__all__ = ['wrap']


def wrap(var):
    if isinstance(var, str):
        var = String(var)
    elif isinstance(var, bool):
        var = Bool(var)
    elif isinstance(var, int):
        var = Int(var)
    elif isinstance(var, float):
        var = Float(var)
    elif isinstance(var, list):
        var = List(var)
    return var


from .var import *
from .string import *
from .num import *
from .list import *
