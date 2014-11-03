import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *
from .expr import *
from xd.build.core.data.wrap import wrap


__all__ = ['Dict']


class Dict(Variable):

    __slots__ = ['amends', 'amend_ifs']

    basetype = dict
    empty = {}

    def __init__(self, value=None, scope=None):
        self.amends = []
        self.amend_ifs = []
        if value is None:
            super(Dict, self).__init__(None, scope)
            return
        super(Dict, self).__init__({}, scope)
        self.set(value)

    def set(self, value):
        value = self.canonicalize(value)
        self.validate_value(value)
        if isinstance(value, dict):
            value = {k: wrap(v) for k, v in value.items()}
        super(Dict, self).set(value)
        self.amends = []

    def get(self):
        value = super(Dict, self).get()
        if value is None:
            return None
        return { k: v.get() if isinstance(v, Variable) else
                 self.scope.eval(v) if isinstance(v, Expression) else v
                 for k, v in value.items() }

    def __setitem__(self, key, value):
        if self.value is None:
            self.value = {}
        if key in self.value:
            self.value[key].set(value)
            return
        value = wrap(value)
        if isinstance(value, Expression):
            raise TypeError(
                'cannot assign Expression to untyped %s value: %s'%(self, key))
        value.scope = self.scope
        self.value[key] = value

    def __getitem__(self, key):
        if self.value is None:
            raise KeyError(key)
        return self.value[key]

    def update(self, value):
        value = self.canonicalize(value)
        self.validate_value(value)
        self.amends.append((self.amend_update, value))

    def amend_update(self, value, amend_value):
        self.validate_value(amend_value)
        amend_value = { k: v.get() if isinstance(v, Variable) else
                        self.scope.eval(v) if isinstance(v, Expression) else v
                        for k, v in amend_value.items() }
        value.update(amend_value)
        return value

    def update_if(self, condition, value):
        condition = self.canonicalize(condition)
        assert isinstance(condition, Expression)
        value = self.canonicalize(value)
        self.validate_value(value)
        if isinstance(value, dict):
            value = {k: wrap(v) for k, v in value.items()}
        self.amend_ifs.append((condition, self.amend_update, value))
