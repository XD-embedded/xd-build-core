import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *
from .expr import *
from .string import *
from .num import *


__all__ = ['Namespace', 'MultiBinding']


class MultiBinding(Exception):
    '''Variable binding to multiple names not allowed.

    For setting one (named) variable to reference the value of another (named)
    variable, you should use Expression() instead.

    Example:
        ns['FOO'] = 'foo'
        ns['ALSO_FOO'] = Expression('FOO')
    '''
    pass


class Namespace(dict):
    """XD-build data namespaces.

    Class for holding a namespace of XD-build data variables.  It is
    implemented as a mapping so it can be used as a locals to eval().
    """

    def __init__(self):
        self.eval_wrapper = EvalWrapper(self)
        super(Namespace, self).__init__(self)

    def __setitem__(self, key, value):
        if key in self:
            self[key].set(value)
            return
        if isinstance(value, str):
            value = String(value)
        elif isinstance(value, bool):
            value = Bool(value)
        elif isinstance(value, int):
            value = Int(value)
        elif isinstance(value, float):
            value = Float(value)
        if isinstance(value, Expression):
            raise TypeError(
                'cannot assign Expression to untyped Variable %s'%(key))
        elif not isinstance(value, Variable):
            raise TypeError('unsupported type for Variable %s: %s'%(
                key, type(value)))
        if getattr(value, 'name', None):
            raise MultiBinding('rename of Variable %s to %s not allowed'%(
                value.name, key))
        value.scope = self
        value.name = key
        super(Namespace, self).__setitem__(key, value)

    def __delitem__(self, key):
        var = super(Namespace, self).__getitem__(key)
        var.name = None
        super(Namespace, self).__delitem__(key)

    def eval(self, expr, g=None):
        if isinstance(expr, Expression):
            expr = expr.code or expr.source
        if g is None:
            g = {}
        return eval(expr, g, self.eval_wrapper)


class EvalWrapper(object):

    def __init__(self, namespace):
        self.namespace = namespace

    def __getitem__(self, key):
        return self.namespace[key].get()
