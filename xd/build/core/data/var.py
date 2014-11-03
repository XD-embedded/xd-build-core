import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .expr import *


__all__ = ['Variable']


class Variable(object):

    __slots__ = ['scope', 'name', 'value', 'set_ifs']

    def __init__(self, value=None):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.value = value
        self.set_ifs = []

    def __str__(self):
        return "%s(%s)"%(self.__class__.__name__,
                         getattr(self, 'name', ''))

    def set(self, value):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.value = value

    def get(self):
        value = self.eval(self.value)
        self.validate_value(value)
        if hasattr(self, 'amend'):
            value = self.amend(value)
        value = self.override(value)
        if hasattr(self, 'amend_if'):
            value = self.amend_if(value)
        return value

    def set_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_value(value)
        self.set_ifs.append((condition, value))

    def override(self, value):
        for (condition, override_value) in reversed(self.set_ifs):
            if self.eval_condition(condition):
                value = self.eval(override_value)
                self.validate_value(value)
                return value
        return value

    def validate_value(self, value):
        if not (value is None or type(value) in (self.basetype, Expression)):
            raise TypeError('invalid type for %s variable <%s>: %s'%(
                self.__class__.__name__, getattr(self, 'name', ''),
                value.__class__.__name__))

    def eval(self, value):
        if isinstance(value, Expression):
            value = self.scope.eval(value)
        return value

    def eval_condition(self, value):
        try:
            return bool(self.scope.eval(value))
        except NameError:
            return False

    def canonicalize(self, value):
        if isinstance(value, Variable):
            value = value.expression()
        return value

    def expression(self):
        assert self.name
        return Expression(self.name)
