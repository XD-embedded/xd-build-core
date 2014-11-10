import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *
from .expr import *


__all__ = ['Sequence']


class Sequence(Variable):

    __slots__ = ['amends', 'amend_ifs']

    def __init__(self, value=None, scope=None):
        self.amends = []
        self.amend_ifs = []
        super(Sequence, self).__init__(value, scope)

    def set(self, value):
        super(Sequence, self).set(value)
        self.amends = []

    def prepend(self, value):
        self.amends.append((self.amend_prepend, self.prepare_value(value)))

    def append(self, value):
        self.amends.append((self.amend_append, self.prepare_value(value)))

    def prepend_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_prepend,
                               self.prepare_value(value)))

    def append_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_append,
                               self.prepare_value(value)))

    def amend_prepend(self, value, amend_value):
        self.validate_value(amend_value)
        return amend_value + value

    def amend_append(self, value, amend_value):
        self.validate_value(amend_value)
        return value + amend_value
