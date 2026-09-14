import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from run_tests import released_labs, run_lab


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "student"
        (self.project / "src").mkdir(parents=True)
        self.lab = self.root / "lab01_example"
        self.lab.mkdir()
        (self.root / "released_labs.json").write_text('["lab01_example"]')

    def suite(self, body):
        (self.lab / "test_example.py").write_text(body)

    def test_pass_and_student_import(self):
        (self.project / "src" / "example.py").write_text("answer = 42")
        self.suite("import unittest, example\nclass T(unittest.TestCase):\n def test_value(self): self.assertEqual(example.answer, 42)\n")
        self.assertEqual(run_lab(self.project, self.lab.name, 5, self.root), 0)

    def test_failure_is_nonzero(self):
        self.suite("import unittest\nclass T(unittest.TestCase):\n def test_value(self): self.fail('deliberate failure')\n")
        self.assertNotEqual(run_lab(self.project, self.lab.name, 5, self.root), 0)

    def test_empty_suite_is_nonzero(self):
        self.suite("# no test cases")
        self.assertNotEqual(run_lab(self.project, self.lab.name, 5, self.root), 0)

    def test_timeout_is_nonzero(self):
        self.suite("import time\ntime.sleep(10)")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertNotEqual(run_lab(self.project, self.lab.name, 0.2, self.root), 0)

    def test_missing_test_files_rejected(self):
        with self.assertRaises(ValueError):
            released_labs(self.root)

    def test_invalid_or_duplicate_names_rejected(self):
        for value in ([], ["../escape"], ["lab01_example", "lab01_example"], [1]):
            (self.root / "released_labs.json").write_text(json.dumps(value))
            with self.subTest(value=value), self.assertRaises(ValueError):
                released_labs(self.root)

    def test_valid_manifest(self):
        self.suite("# file is present; case count is checked when run")
        self.assertEqual(released_labs(self.root), [self.lab.name])
