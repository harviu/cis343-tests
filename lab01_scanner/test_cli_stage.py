"""Scanner-mode CLI contract applies only while Lab 1 is the current stage."""
import os
import unittest
from support import cli


@unittest.skipUnless(os.environ.get('CIS343_STAGE') == 'lab01_scanner',
                     'Later lab changes CLI output; scanner API tests still run')
class ScannerCliTests(unittest.TestCase):
    def test_file_prints_scanned_tokens(self):
        result = cli('var greeting = "hello";')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        lines = result.stdout.strip().splitlines()
        expected = [('VAR', 'var', 'None'), ('IDENTIFIER', 'greeting', 'None'),
                    ('EQUAL', '=', 'None'), ('STRING', '"hello"', 'hello'),
                    ('SEMICOLON', ';', 'None'), ('EOF', '', 'None')]
        self.assertEqual(len(lines), len(expected), result.stdout)
        for line, fields in zip(lines, expected):
            for field in fields:
                self.assertIn(field, line)
