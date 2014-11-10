import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


import ast


__all__ = ['Expression']


class Expression(object):

    def __init__(self, expr, scope=None, constructor=None):
        self.scope = scope
        self.constructor = constructor
        if isinstance(expr, ast.expr):
            e = ast.Expression()
            ast.copy_location(e, expr)
            e.body = expr
            expr = e
        if isinstance(expr, str):
            #self.source = expr
            self.code = compile(expr, '<>', 'eval')
        elif isinstance(expr, ast.Expression):
            #self.source = expr
            self.code = compile(expr, '<>', 'eval')
        else:
            raise TypeError('invalid expr type: %s'%(type(expr)))

    def set_scope(self, scope):
        self.scope = scope

    def get(self):
        return self.scope.eval(self)
