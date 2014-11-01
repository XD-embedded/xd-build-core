import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .expr import *
import collections
import copy


__all__ = ['Variable']


class Variable(object):

    __slots__ = ['scope', 'name', 'value', 'set_ifs']

    def __init__(self, value=None):
        if isinstance(value, Variable):
            value = value.expression()
        assert self.isvalid(value)
        self.value = value
        self.set_ifs = []

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
        value = self.override(value)
        if hasattr(self, 'amend_if'):
            value = self.amend_if(value)
        return value

    def set_if(self, condition, value):
        if isinstance(condition, Variable):
            condition = condition.expression()
        assert isinstance(condition, Expression)
        if isinstance(value, Variable):
            value = value.expression()
        if not self.isvalid(value):
            raise TypeError('cannot append %s to %s'%(type(value), type(self)))
        self.set_ifs.append((condition, value))

    def override(self, value):
        for (condition, override_value) in reversed(self.set_ifs):
            if self.condition_is_true(condition):
                assert self.isvalid(override_value)
                if isinstance(override_value, Expression):
                    override_value = self.scope.eval(override_value)
                if not isinstance(override_value, self.basetype):
                    raise TypeError(
                        "unsupported append operation: %s to %s"%(
                            type(override_value), type(value)))
                return override_value
        return value

    def condition_is_true(self, condition):
        try:
            return bool(self.scope.eval(condition))
        except NameError:
            return False

    def isvalid(self, value):
        return (value is None or
                isinstance(value, self.basetype) or
                isinstance(value, Expression))

    def expression(self):
        assert self.name
        return Expression(self.name)
