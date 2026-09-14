import os
import unittest
from support import cli, assert_lines


@unittest.skipUnless(os.environ.get('CIS343_STAGE') == 'lab04_interpreter',
                     'Later lab requires statements; expression evaluation tests still run')
class CalculatorCliTests(unittest.TestCase):
    def test_calculator_pipeline(self):
        result = cli('(1 + 2) * 3')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        assert_lines(self, result.stdout, [9])

    def test_type_error_is_reported_without_traceback(self):
        result = cli('-"x"')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback (most recent call last)', result.stdout + result.stderr)
        self.assertRegex((result.stdout + result.stderr).lower(), 'operand|number|type')
