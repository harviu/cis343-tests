import unittest
from support import parse_expression
from interpreter import Interpreter
from error_handler import ErrorHandler, LoxRuntimeError


class InterpreterTests(unittest.TestCase):
    def evaluate(self, source):
        expression = parse_expression(source)
        self.assertFalse(ErrorHandler.had_error)
        return Interpreter().evaluate(expression)

    def test_grouping_and_precedence(self):
        self.assertEqual(self.evaluate('(1 + 2) * 3 - 4 / 2'), 7)

    def test_negative_number(self):
        self.assertEqual(self.evaluate('-3'), -3)

    def test_double_negation(self):
        self.assertEqual(self.evaluate('--3'), 3)

    def test_logical_not_true(self):
        self.assertIs(self.evaluate('!true'), False)

    def test_logical_not_false(self):
        self.assertIs(self.evaluate('!false'), True)

    def test_logical_not_nil(self):
        self.assertIs(self.evaluate('!nil'), True)

    def test_string_concatenation(self):
        self.assertEqual(self.evaluate('"hello " + "world"'), 'hello world')

    def test_string_equality(self):
        self.assertIs(self.evaluate('"same" == "same"'), True)

    def test_nil_equality(self):
        self.assertIs(self.evaluate('nil == nil'), True)

    def test_division_by_zero_is_language_error(self):
        with self.assertRaises(LoxRuntimeError):
            self.evaluate('1 / 0')


def value_test(source, expected):
    def test(self):
        actual = self.evaluate(source)
        if isinstance(expected, bool):
            self.assertIs(actual, expected)
        else:
            self.assertAlmostEqual(actual, expected)
    return test

for name, source, expected in [
    ('add','3 + 2',5),('subtract','3 - 2',1),('multiply','3 * 2',6),
    ('divide','5 / 2',2.5),('equal_true','3 == 3',True),('equal_false','3 == 2',False),
    ('not_equal','3 != 2',True),('greater','3 > 2',True),('greater_false','2 > 3',False),
    ('greater_equal','3 >= 3',True),('less','2 < 3',True),('less_equal','3 <= 3',True)]:
    setattr(InterpreterTests,'test_'+name,value_test(source,expected))


def error_test(source):
    def test(self):
        with self.assertRaises(LoxRuntimeError):
            self.evaluate(source)
    return test

for name, source in [('negate_string','-"x"'),('mixed_add','"x" + 1'),
                     ('subtract_string','"x" - 1'),('multiply_string','"x" * 2'),
                     ('divide_string','"x" / 2'),('compare_string','"x" < 2'),
                     ('negate_boolean','-true')]:
    setattr(InterpreterTests,'test_error_'+name,error_test(source))
