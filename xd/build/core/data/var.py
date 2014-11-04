import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .expr import *


__all__ = ['Variable']


class Variable(object):

    __slots__ = ['scope', 'name', 'value', 'set_ifs']

    def __init__(self, value=None, scope=None):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.value = value
        self.scope = scope
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
        if hasattr(self, 'amends'):
            value = self.amend(value)
        value = self.override(value)
        if hasattr(self, 'amend_ifs'):
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

    def amend(self, value):
        for amend_func, amend_value in self.amends:
            value = self.amend_it(value, amend_func, amend_value)
        return value

    def amend_if(self, value):
        for (condition, amend_func, amend_value) in self.amend_ifs:
            if not self.eval_condition(condition):
                continue
            value = self.amend_it(value, amend_func, amend_value)
        return value

    def amend_it(self, value, amend_func, amend_value):
        amend_value = self.eval(amend_value)
        if amend_value is None:
            return value
        if value is None:
            try:
                value = self.empty.copy()
            except AttributeError:
                value = self.empty
        return amend_func(value, amend_value)

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
        try:
            name = self.name
        except AttributeError:
            return self.get()
        return Expression(self.name)
