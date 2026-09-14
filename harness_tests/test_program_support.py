import importlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


class ProgramSupportTests(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {'CIS343_STUDENT_ROOT': tempfile.gettempdir()}):
            self.support = importlib.import_module('support')

    def test_numeric_display_variations(self):
        self.support.assert_lines(self, '3.0\nTrue\nnil\ntext\n', [3, True, None, 'text'])

    def test_wrong_result_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.support.assert_lines(self, '4', [3])

    def test_extra_output_is_rejected(self):
        with self.assertRaises(AssertionError):
            self.support.assert_lines(self, '3\nextra', [3])

    def test_traceback_is_not_an_accepted_language_error(self):
        result = subprocess.CompletedProcess([], 1, '', 'Traceback (most recent call last):\nTypeError: bad operand')
        with patch.object(self.support, 'cli', return_value=result), self.assertRaises(AssertionError):
            self.support.check_program(self, {'source':'bad', 'error':'operand'})

    def test_wrong_diagnostic_is_rejected(self):
        result = subprocess.CompletedProcess([], 65, 'Expect expression', '')
        with patch.object(self.support, 'cli', return_value=result), self.assertRaises(AssertionError):
            self.support.check_program(self, {'source':'bad', 'error':'undefined'})

    def test_success_status_cannot_satisfy_error_case(self):
        result = subprocess.CompletedProcess([], 0, 'undefined variable', '')
        with patch.object(self.support, 'cli', return_value=result), self.assertRaises(AssertionError):
            self.support.check_program(self, {'source':'bad', 'error':'undefined'})
