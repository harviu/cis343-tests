import unittest
from support import parse_program
from error_handler import ErrorHandler
from resolver import Resolver


class ResolverTests(unittest.TestCase):
    def test_records_environment_distances(self):
        class Recorder:
            def __init__(self):
                self.depths = []
            def resolve(self, expression, depth):
                self.depths.append((expression.name.lexeme, depth))
        recorder = Recorder()
        statements = parse_program('{ var a=1; { var b=2; print a; print b; } }')
        Resolver(recorder).resolve(statements)
        self.assertFalse(ErrorHandler.had_error)
        self.assertIn(('a', 1), recorder.depths)
        self.assertIn(('b', 0), recorder.depths)
