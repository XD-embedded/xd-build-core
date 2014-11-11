import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .expr import Expression
import types


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
    elif type(var) == list:
        var = List(var)
    elif type(var) == dict:
        var = Dict(var)
    elif type(var) == types.FunctionType:
        var = Function(var)
    elif isinstance(var, Expression) and var.constructor:
        var = var.constructor(var)
    return var


from .var import *
from .string import *
from .num import *
from .list import *
from .dict import *
from .func import *
