import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *
from .expr import *


__all__ = ['Sequence']


class Sequence(Variable):

    __slots__ = ['amends', 'amend_ifs']

    def __init__(self, value=None):
        self.amends = []
        self.amend_ifs = []
        super(Sequence, self).__init__(value)

    def set(self, value):
        super(Sequence, self).set(value)
        self.amends = []

    def prepend(self, value):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amends.append((self.amend_prepend, value))

    def append(self, value):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amends.append((self.amend_append, value))

    def amend(self, value):
        for amend_func, amend_value in self.amends:
            value = self.amend_it(value, amend_func, amend_value)
        return value

    def amend_it(self, value, amend_func, amend_value):
        amend_value = self.eval(amend_value)
        if amend_value is None:
            return value
        if value is None:
            value = self.empty
        return amend_func(value, amend_value)

    def amend_prepend(self, value, amend_value):
        self.validate_value(amend_value)
        return amend_value + value

    def amend_append(self, value, amend_value):
        self.validate_value(amend_value)
        return value + amend_value

    def prepend_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amend_ifs.append((condition, self.amend_prepend, value))

    def append_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amend_ifs.append((condition, self.amend_append, value))

    def amend_if(self, value):
        for (condition, amend_func, amend_value) in self.amend_ifs:
            if not self.eval_condition(condition):
                continue
            value = self.amend_it(value, amend_func, amend_value)
        return value
