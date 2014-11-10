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
        if not value:
            return value
        value = [v.get() if isinstance(v, Variable) else v
                 for v in value]
        value = [self.eval(v) if isinstance(v, Expression) else v
                 for v in value]
        for v in value:
            self.validate_item(v)
        sort_reverse = getattr(self, 'sorted', None)
        if sort_reverse is not None:
            value.sort(reverse=sort_reverse)
        return value

    def prepare_value(self, value):
        value = super(List, self).prepare_value(value)
        if isinstance(value, list):
            value = [self.prepare_item(v) for v in value]
        return value

    def prepare_item(self, value):
        """Prepare value for use as List item value.

        Check validity of value for use as a List item value, and make
        necessary adjustments for its use as such.
        """
        if isinstance(value, Variable):
            try:
                name = value.name
            except AttributeError:
                raise TypeError('cannot use anonymous %s as List item'%(
                    value.__class__.__name__))
            value = Expression(name)
        if not type(value) in (type(None), Expression,
                               str, bool, int, float, tuple):
            raise TypeError('invalid type for List <%s> element: %s'%(
                getattr(self, 'name', ''), value.__class__.__name__))
        return value

    def validate_item(self, value):
        if not type(value) in (type(None), str, bool, int, float, tuple):
            raise TypeError('invalid type for %s element in <%s>: %s'%(
                self.__class__.__name__, getattr(self, 'name', ''),
                value.__class__.__name__))

    def prepend(self, value):
        self.amends.append((self.amend_prepend, [self.prepare_item(value)]))

    def append(self, value):
        self.amends.append((self.amend_append, [self.prepare_item(value)]))

    def prepend_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_prepend,
                               [self.prepare_item(value)]))

    def append_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_append,
                               [self.prepare_item(value)]))

    def remove(self, value):
        self.amends.append((self.amend_remove, self.prepare_item(value)))

    def remove_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_remove,
                               self.prepare_item(value)))

    def amend_remove(self, value, amend_value):
        self.validate_item(amend_value)
        try:
            value.remove(amend_value)
        except ValueError:
            pass
        return value

    def extend(self, value):
        self.amends.append((self.amend_extend, self.prepare_value(value)))

    def extend_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_extend,
                               self.prepare_value(value)))

    def amend_extend(self, value, amend_value):
        self.validate_value(amend_value)
        value.extend(amend_value)
        return value

    def sort(self, reverse=False):
        assert isinstance(reverse, int)
        self.sorted = reverse
