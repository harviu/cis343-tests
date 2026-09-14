"""Shared assertions for the Python Lox reference interfaces."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

PROJECT = Path(os.environ['CIS343_STUDENT_ROOT']).resolve()
TIMEOUT = 5


def reset_errors():
    from error_handler import ErrorHandler
    ErrorHandler.had_error = False
    ErrorHandler.had_runtime_error = False


def parse_expression(source):
    from scanner import Scanner
    from parser import Parser
    reset_errors()
    parser = Parser(Scanner(source).scan_tokens())
    # parse() changes from expression -> statement-list in Lab 5;
    # expression() remains the cumulative expression API.
    return parser.expression()


def parse_program(source):
    from scanner import Scanner
    from parser import Parser
    reset_errors()
    return Parser(Scanner(source).scan_tokens()).parse()


def cli(source):
    with tempfile.TemporaryDirectory(prefix='cis343-case-') as temp:
        script = Path(temp) / 'case.lox'
        script.write_text(source, encoding='utf-8')
        try:
            return subprocess.run([sys.executable, str(PROJECT / 'src/lox.py'), str(script)],
                                  cwd=PROJECT, capture_output=True, text=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired as error:
            raise AssertionError(f'Program exceeded {TIMEOUT}s: {source}') from error


def assert_lines(test, actual, expected):
    lines = actual.strip().splitlines()
    test.assertEqual(len(lines), len(expected), f'Expected {expected!r}, got {actual!r}')
    for line, value in zip(lines, expected):
        if isinstance(value, bool):
            test.assertEqual(line.lower(), str(value).lower())
        elif value is None:
            test.assertEqual(line, 'nil')
        elif isinstance(value, (int, float)):
            try:
                numeric = float(line)
            except ValueError:
                test.fail(f'Expected number {value}, got {line!r}')
            test.assertTrue(math.isfinite(numeric))
            test.assertAlmostEqual(numeric, value, places=7)
        else:
            test.assertEqual(line, value)


def check_program(test, case):
    result = cli(case['source'])
    combined = result.stdout + result.stderr
    test.assertNotIn('Traceback (most recent call last)', combined, combined)
    if 'error' in case:
        test.assertNotEqual(result.returncode, 0, combined)
        test.assertRegex(combined.lower(), case['error'], combined)
    else:
        test.assertEqual(result.returncode, 0, combined)
        test.assertEqual(result.stderr.strip(), '', combined)
        if case.get('clock'):
            lines = result.stdout.strip().splitlines()
            test.assertEqual(len(lines), 1, combined)
            value = float(lines[0])
            test.assertTrue(math.isfinite(value) and value >= 0, combined)
        else:
            assert_lines(test, result.stdout, case['output'])


def install_program_cases(namespace, path):
    """Expose one named unittest per data case for individual feedback."""
    cases = json.loads(Path(path).read_text())
    names = set()
    cls = type('ProgramTests', (unittest.TestCase,), {'__module__': namespace['__name__']})
    for case in cases:
        name = case['name']
        if not re.fullmatch('[a-z][a-z0-9_]+', name) or name in names:
            raise ValueError(f'Invalid/duplicate case name: {name}')
        names.add(name)
        if not isinstance(case['source'], str) or sum(key in case for key in ('output','error','clock')) != 1:
            raise ValueError(f'Invalid case: {name}')
        def check(self, case=case):
            check_program(self, case)
        check.__doc__ = case.get('requirement', name)
        setattr(cls, 'test_' + name, check)
    if not cases:
        raise ValueError('No program cases')
    namespace['ProgramTests'] = cls
