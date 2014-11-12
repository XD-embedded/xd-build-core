import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .var import *
import types
import inspect
import ast
import astunparse


__all__ = ['Function']


class Function(Variable):

    __slots__ = ['source']

    basetype = types.FunctionType

    def __init__(self, value=None, scope=None):
        self.source = {}
        super(Function, self).__init__(value, scope)
    
    # FIXME: keep in code format, and only produce source code when
    # calling:
    def get_source(self):
        code = self.get()
        if code is None:
            return None
        assert isinstance(code, types.FunctionType)
        if not code in self.source:
            self.set_source(inspect.getsource(code), function=code)
        return self.source[code]

    def set_source(self, source, function=None):
        if function is None:
            function = self.value
        assert isinstance(function, types.FunctionType)
        if isinstance(source, str):
            source = ast.parse(source)
            assert isinstance(source, ast.Module)
            assert isinstance(source.body, list) and len(source.body) == 1
            source = source.body[0]
        assert isinstance(source, ast.FunctionDef)
        source = astunparse.unparse(source)
        source = '\n' + source.strip('\n') + '\n'
        self.source[function] = source
