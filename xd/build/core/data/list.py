import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .sequence import *
from .var import *
from .expr import *
import copy


__all__ = ['List']


class List(Sequence):

    __slots__ = ['sorted']

    basetype = list
    empty = []

    def get(self):
        value = super(Sequence, self).get()
        if value is None:
            return None
        value = [v.get() if isinstance(v, Variable) else
                 self.scope.eval(v) if isinstance(v, Expression) else v
                 for v in value]
        sort_reverse = getattr(self, 'sorted', None)
        if sort_reverse is not None:
            value.sort(reverse=sort_reverse)
        return value

    def validate_element(self, value):
        if not type(value) in (str, bool, int, float, tuple, Expression):
            raise TypeError('invalid type for %s element in <%s>: %s'%(
                self.__class__.__name__, getattr(self, 'name', ''),
                value.__class__.__name__))

    def prepend(self, value):
        value = self.canonicalize(value)
        self.validate_element(value)
        self.amends.append((self.amend_prepend, [value]))

    def append(self, value):
        value = self.canonicalize(value)
        self.validate_element(value)
        self.amends.append((self.amend_append, [value]))

    def prepend_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_element(value)
        self.amend_ifs.append((condition, self.amend_prepend, [value]))

    def append_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_element(value)
        self.amend_ifs.append((condition, self.amend_append, [value]))

    def remove(self, value):
        if isinstance(value, Variable):
            value = value.expression()
        self.amends.append((self.amend_remove, value))

    def remove_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_element(value)
        self.amend_ifs.append((condition, self.amend_remove, value))

    def amend_remove(self, value, amend_value):
        self.validate_element(amend_value)
        try:
            value2 = copy.copy(value)
            value2.remove(amend_value)
            value = value2
        except ValueError:
            pass
        return value

    def extend(self, value):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amends.append((self.amend_extend, value))

    def extend_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amend_ifs.append((condition, self.amend_extend, value))

    def amend_extend(self, value, amend_value):
        self.validate_value(amend_value)
        value = copy.copy(value)
        value.extend(amend_value)
        return value

    def sort(self, reverse=False):
        assert isinstance(reverse, int)
        self.sorted = reverse
