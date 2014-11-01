import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *
from .expr import *


__all__ = ['Sequence']


class Sequence(Variable):

    __slots__ = ['prepends', 'appends', 'prepend_ifs', 'append_ifs']

    def __init__(self, value=None):
        self.prepends = []
        self.appends  = []
        self.prepend_ifs = []
        self.append_ifs  = []
        super(Sequence, self).__init__(value)

    def __getitem__(self, index):
        return self.get().__getitem__(index)

    def __len__(self):
        return self.get().__len__()

    def __contains__(self, item):
        return self.get().__contains__(item)

    def index(self, sub, start=0, end=None):
        if end is None:
            return self.get().index(sub, start)
        else:
            return self.get().index(sub, start, end)

    def count(self, sub):
        return self.get().count(sub)

    def set(self, value):
        super(Sequence, self).set(value)
        self.prepends = []
        self.appends  = []

    def prepend(self, value):
        if isinstance(value, Variable):
            value = value.expression()
        if not self.isvalid(value):
            raise TypeError('cannot prepend %s to %s'%(type(value), type(self)))
        self.prepends.append(value)

    def append(self, value):
        if isinstance(value, Variable):
            value = value.expression()
        if not self.isvalid(value):
            raise TypeError('cannot append %s to %s'%(type(value), type(self)))
        self.appends.append(value)

    def amend_prepend(self, value, amend_value):
        assert self.isvalid(amend_value)
        if isinstance(amend_value, Expression):
            amend_value = self.scope.eval(amend_value)
        if amend_value is None:
            return value
        if value is None:
            value = self.empty
        if isinstance(amend_value, self.basetype):
            value = amend_value + value
        else:
            raise TypeError(
                "unsupported prepend operation: %s to %s"%(
                    type(amend_value), type(value)))
        return value

    def amend_append(self, value, amend_value):
        assert self.isvalid(amend_value)
        if isinstance(amend_value, Expression):
            amend_value = self.scope.eval(amend_value)
        if amend_value is None:
            return value
        if value is None:
            value = self.empty
        if isinstance(amend_value, self.basetype):
            value = value + amend_value
        else:
            raise TypeError(
                "unsupported append operation: %s to %s"%(
                    type(amend_value), type(value)))
        return value

    def amend(self, value):
        for amend_value in self.prepends:
            value = self.amend_prepend(value, amend_value)
        for amend_value in self.appends:
            value = self.amend_append(value, amend_value)
        return value

    def prepend_if(self, condition, value):
        if isinstance(condition, Variable):
            condition = condition.expression()
        assert isinstance(condition, Expression)
        if isinstance(value, Variable):
            value = value.expression()
        if not self.isvalid(value):
            raise TypeError('cannot prepend %s to %s'%(type(value), type(self)))
        self.prepend_ifs.append((condition, value))

    def append_if(self, condition, value):
        if isinstance(condition, Variable):
            condition = condition.expression()
        assert isinstance(condition, Expression)
        if isinstance(value, Variable):
            value = value.expression()
        if not self.isvalid(value):
            raise TypeError('cannot append %s to %s'%(type(value), type(self)))
        self.append_ifs.append((condition, value))

    def amend_if(self, value):
        for (condition, amend_value) in self.prepend_ifs:
            if self.condition_is_true(condition):
                value = self.amend_prepend(value, amend_value)
        for (condition, amend_value) in self.append_ifs:
            if self.condition_is_true(condition):
                value = self.amend_append(value, amend_value)
        return value
