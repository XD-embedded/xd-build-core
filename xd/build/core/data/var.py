import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .expr import *


__all__ = ['Variable']


class Variable(object):

    __slots__ = ['scope', 'name', 'value', 'set_ifs']

    def __init__(self, value=None, scope=None):
        self.scope = scope
        self.set(value)
        self.set_ifs = []

    def __str__(self):
        return "%s(%s)"%(self.__class__.__name__,
                         getattr(self, 'name', ''))

    def set_scope(self, scope):
        self.scope = scope

    def set(self, value):
        self.value = self.prepare_value(value)

    def get(self):
        value = self.eval(self.value, self.validate_value)
        if hasattr(self, 'amends'):
            value = self.amend(value)
        value = self.override(value)
        if hasattr(self, 'amend_ifs'):
            value = self.amend_if(value)
        return value

    def set_if(self, condition, value):
        self.set_ifs.append((self.prepare_condition(condition),
                             self.prepare_value(value)))

    def override(self, value):
        for (condition, override_value) in reversed(self.set_ifs):
            if self.eval_condition(condition):
                return self.eval(override_value, self.validate_value)
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
            value = self.empty
        try:
            value = value.copy()
        except AttributeError:
            pass
        return amend_func(value, amend_value)

    def eval(self, value, validate=None):
        if isinstance(value, Expression):
            assert self.scope is not None
            value = self.scope.eval(value)
        if validate:
            validate(value)
        return value

    def prepare_value(self, value):
        """Prepare value for use as Variable stored value.

        Check validity of value for use as a stored value for Variable, and
        make necessary adjustments for its use as such.
        """
        if isinstance(value, Variable):
            try:
                name = value.name
            except AttributeError:
                raise TypeError('cannot use anonymous %s as %s value'%(
                    value.__class__.__name__, self.__class__.__name__))
            value = Expression(name)
        if isinstance(value, Expression):
            value.set_scope(self.scope)
        if not type(value) in (type(None), self.basetype, Expression):
            raise TypeError('invalid type for %s variable <%s>: %s'%(
                self.__class__.__name__, getattr(self, 'name', ''),
                value.__class__.__name__))
        return value

    def validate_value(self, value):
        """Validate Variable value.

        Check validity of value as proper Variable value..
        """
        if not type(value) in (type(None), self.basetype):
            raise TypeError('invalid type for %s variable <%s>: %s'%(
                self.__class__.__name__, getattr(self, 'name', ''),
                value.__class__.__name__))

    def eval_condition(self, condition):
        if isinstance(condition, Expression):
            assert self.scope is not None
            try:
                condition = self.scope.eval(condition)
            except NameError:
                return False
        return bool(condition)

    def prepare_condition(self, value):
        """Prepare value for use as Variable condition value.

        Check validity of value for use as a condition value for Variable, and
        make necessary adjustments for its use as such.
        """
        if isinstance(value, Variable):
            try:
                name = value.name
            except AttributeError:
                raise TypeError('cannot use anonymous %s as %s condition'%(
                    value.__class__.__name__, self.__class__.__name__))
            value = Expression(name)
        if isinstance(value, Expression):
            value.set_scope(self.scope)
        return value
