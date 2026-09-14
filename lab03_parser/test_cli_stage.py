import os
import unittest
from support import cli


@unittest.skipUnless(os.environ.get('CIS343_STAGE') == 'lab03_parser',
                     'Later lab changes CLI output; expression parsing tests still run')
class ParserCliTests(unittest.TestCase):
    def test_scanner_parser_printer_pipeline(self):
        result = cli('(1 + 2) * 3')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), '(* (group (+ 1.0 2.0)) 3.0)')
