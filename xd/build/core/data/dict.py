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
        super(Dict, self).__init__(value, scope)

    def set_scope(self, scope):
        if self.value:
            for value in self.value.values():
                if isinstance(value, Variable):
                    value.set_scope(scope)
        for (condition, value) in self.set_ifs:
            for v in value.values():
                if isinstance(v, Variable):
                    v.set_scope(scope)
        for (func, value) in self.amends:
            for v in value.values():
                if isinstance(v, Variable):
                    v.set_scope(scope)
        for (condition, func, value) in self.amend_ifs:
            for v in value.values():
                if isinstance(v, Variable):
                    v.set_scope(scope)
        super(Dict, self).set_scope(scope)

    def set(self, value):
        super(Dict, self).set(value)
        self.amends = []


    def __setitem__(self, key, value):
        if self.value is None:
            self.value = {}
        if key in self.value:
            self.value[key].set(value)
            return
        self.value[key] = self.prepare_item(value)

    def __getitem__(self, key):
        if self.value is None:
            raise KeyError(key)
        return self.value[key]

    def prepare_value(self, value):
        value = super(Dict, self).prepare_value(value)
        if isinstance(value, dict):
            value = {k: self.prepare_item(v) for k, v in value.items()}
            for v in value.values():
                if isinstance(v, (Variable, Expression)):
                    v.set_scope(self.scope)
        return value

    def prepare_item(self, value):
        """Prepare value for use as Dict item value.

        Check validity of value for use as a Dict item value, and make
        necessary adjustments for its use as such.
        """
        if isinstance(value, Variable):
            if hasattr(value, 'name'):
                value = Expression(value.name)
            #else:
            #    # FIXME: is this a way to protect against double assignment of
            #    # Variable instances to dicts?
            #    assert not hasattr(value, 'scope')
        value = wrap(value)
        if isinstance(value, (Expression, Variable)):
            value.set_scope(self.scope)
        elif not isinstance(value, type(None)):
            raise TypeError('invalid type for Dict <%s> item: %s'%(
                getattr(self, 'name', ''), value.__class__.__name__))
        return value

    def validate_item(self, value):
        if not type(value) in (type(None), str, bool, int, float, list, dict):
            raise TypeError('invalid type for %s item in <%s>: %s'%(
                self.__class__.__name__, getattr(self, 'name', ''),
                value.__class__.__name__))

    def update(self, value):
        self.amends.append((self.amend_update, self.prepare_value(value)))

    def update_if(self, condition, value):
        self.amend_ifs.append((self.prepare_condition(condition),
                               self.amend_update,
                               self.prepare_value(value)))

    def amend_update(self, value, amend_value):
        self.validate_value(amend_value)
        value.update(amend_value)
        return value

    def eval(self, value, validate=None):
        if validate:
            validate_value = validate
            validate_item = self.validate_item
        else:
            validate_value = validate_item = None
        value = super(Dict, self).eval(value, validate_value)
        if not value:
            return value
        if isinstance(value, dict):
            value = {k: v.get() if isinstance(v, Variable) else v
                     for k, v in value.items()}
            value = {k: self.eval(v) if isinstance(v, Expression) else v
                     for k, v in value.items()}
            if validate_item:
                for v in value.values():
                    self.validate_item(v)
        assert not isinstance(value, Expression)
        return value
