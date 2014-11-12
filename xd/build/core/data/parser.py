import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .namespace import *
from .expr import *
from .string import *
from .num import *
from .list import *
from .dict import *
import ast


__all__ = ['Parser', 'SyntaxError']


class SyntaxError(Exception):
    pass


class Parser(object):

    constructors = ['String', 'Bool', 'Int', 'Float', 'List', 'Dict']

    def __init__(self):
        self.backlog = ast.Module()
        self.backlog.body = []

    def parse(self, path):
        self.namespace = Namespace()
        self.expression_store = ExpressionStore('_expr', self.namespace)
        self.globals = {
            '_expr': self.expression_store.expressions,
            '_namespace': self.namespace
        }
        for constructor in self.constructors:
            self.globals[constructor] = eval(constructor)
        source = open(path).read()
        statements = ast.parse(source, path)
        for statement in statements.body:
            self.parse_statement(statement)
        self.process_backlog(self.globals, self.namespace, path)
        return self.namespace

    def parse_statement(self, statement):
        if isinstance(statement, ast.Assign):
            self.parse_assignment(statement)
        elif isinstance(statement, ast.Expr):
            self.parse_expression(statement)
        elif isinstance(statement, ast.FunctionDef):
            self.parse_functiondef(statement)
        else:
            raise SyntaxError('unsupported statement: %s'%(
                statement.__class__.__name__))

    def parse_assignment(self, statement):
        statement.value = self.parse_value(statement.value)
        for i in range(len(statement.targets)):
            if isinstance(statement.targets[i], ast.Subscript):
                subscript = self.expression_store.store(
                    statement.targets[i].slice.value)
                if isinstance(subscript, ast.Subscript):
                    statement.targets[i].slice.value = ast.Call(
                        func=ast.Attribute(
                            ctx=ast.Load(), value=subscript, attr='get'),
                        args=[], keywords=[])
                    ast.fix_missing_locations(statement.targets[i])
        self.backlog.body.append(statement)

    def parse_expression(self, statement):
        assert isinstance(statement.value, ast.Call)
        statement.value.args = [
            self.parse_value(arg, strwrap=False)
            for arg in statement.value.args]
        for i in range(len(statement.value.keywords)):
            keyword = statement.value.keywords[i]
            keyword.value = self.expression_store.store(keyword.value)
        self.backlog.body.append(statement)

    def parse_functiondef(self, statement):
        self.backlog.body.append(statement)
        set_source_statement = ast.copy_location(ast.Expr(ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=statement.name, ctx=ast.Load()),
                attr='set_source', ctx=ast.Load()),
            args=[self.expression_store.store(statement)],
            keywords=[])), statement)
        ast.fix_missing_locations(set_source_statement)
        self.backlog.body.append(set_source_statement)

    def parse_value(self, value, strwrap=True):
        if type(value) in (ast.Str, ast.Num, ast.NameConstant):
            return value
        elif isinstance(value, ast.List):
            value.elts = [self.parse_value(e) for e in value.elts]
            return value
        elif isinstance(value, ast.Dict):
            value.values = [self.parse_value(v) for v in value.values]
            return value
        elif (strwrap and
              isinstance(value, ast.BinOp) and
              isinstance(value.left, ast.Str) and
              isinstance(value.op, ast.Mod)):
            return self.expression_store.store(value, String)
        elif (strwrap and
              isinstance(value, ast.Call) and
              isinstance(value.func, ast.Attribute) and
              isinstance(value.func.value, ast.Str)):
            return self.expression_store.store(value, String)
        elif (isinstance(value, ast.Call) and
              hasattr(value.func, 'id') and
              value.func.id in self.constructors):
            value.args = [ self.expression_store.store(arg)
                           for arg in value.args]
            return value
        else:
            return self.expression_store.store(value)

    def process_backlog(self, g, l, path):
        if not self.backlog.body:
            return
        code = compile(self.backlog, path, 'exec')
        exec(code, g, l)


class ExpressionStore(object):

    def __init__(self, id, scope):
        self.expressions = []
        self.id = id
        self.scope = scope

    def store(self, value, constructor=None):
        if type(value) in (ast.Str, ast.Num, ast.List, ast.Dict,
                           ast.NameConstant):
            return value
        if isinstance(value, ast.FunctionDef):
            expr = value
        else:
            expr = Expression(value, self.scope, constructor)
        self.expressions.append(expr)
        ref = ast.Subscript()
        ref.ctx = ast.Load()
        ref.slice = ast.Index()
        ref.slice.value = ast.Num()
        ref.slice.value.n = len(self.expressions) - 1
        ref.value = ast.Name()
        ref.value.ctx = ast.Load()
        ref.value.id = self.id
        ast.fix_missing_locations(ref)
        return ref
