import unittest
from support import parse_program
from error_handler import ErrorHandler


def nodes(value):
    if isinstance(value, list):
        for item in value:
            yield from nodes(item)
    elif value is not None and value.__class__.__module__ in ('stmt', 'expr'):
        yield value
        for child in vars(value).values():
            yield from nodes(child)


class DesugaringTests(unittest.TestCase):
    def test_for_becomes_while(self):
        tree = parse_program('for (var i=0; i<3; i=i+1) print i;')
        self.assertFalse(ErrorHandler.had_error)
        kinds = [type(node).__name__ for node in nodes(tree)]
        self.assertIn('While', kinds)
        self.assertIn('Var', kinds)
        self.assertIn('Assign', kinds)
        self.assertNotIn('For', kinds, 'Lab 6 requires desugaring rather than a runtime For node')

    def test_omitted_condition_becomes_true(self):
        tree = parse_program('for (;;) print 1;')
        self.assertFalse(ErrorHandler.had_error)
        loops = [n for n in nodes(tree) if type(n).__name__ == 'While']
        self.assertEqual(len(loops), 1)
        self.assertIs(loops[0].condition.value, True)
