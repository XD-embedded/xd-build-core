import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .expr import *
import collections
import copy


__all__ = ['Variable']


class Variable(object):

    __slots__ = ['scope', 'name', 'value']

    def __init__(self, value=None):
        if isinstance(value, Variable):
            value = value.expression()
        assert self.isvalid(value)
        self.value = value

    def __str__(self):
        return str(self.get())

    def set(self, value):
        if isinstance(value, Variable):
            value = value.expression()
        if self.isvalid(value):
            self.value = value
        else:
            raise TypeError("cannot set %r to %s value"%(
                self, type(value).__name__))

    def get(self):
        value = self.value
        if isinstance(value, Expression):
            value = self.scope.eval(value)
        if not (value is None or isinstance(value, self.basetype)):
            raise TypeError("invalid type in %s %s value: %s"%(
                type(self).__name__, self.name or '<>', type(value).__name__))
        if hasattr(self, 'amend'):
            value = self.amend(value)
        # TODO: override_if handling
        # TODO: amend_if handling
        return value

    def isvalid(self, value):
        return (value is None or
                isinstance(value, self.basetype) or
                isinstance(value, Expression))

    def expression(self):
        assert self.name
        return Expression(self.name)
