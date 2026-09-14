import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import run_tests


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'src').mkdir()
        (self.root / 'released_labs.json').write_text('["lab01_example"]')
        (self.root / 'lab_branches.json').write_text('{"lab01_example":"one","lab02_example":"two"}')
        for name in ('lab01_example','lab02_example'):
            (self.root / name).mkdir()
            (self.root / name / 'test_case.py').write_text('import unittest\n')

    def invoke(self, *args):
        with patch.object(run_tests, 'ROOT', self.root), \
             patch.object(run_tests, 'released_labs', return_value=['lab01_example']), \
             patch.object(run_tests, 'run_lab', return_value=0) as runner, \
             patch.object(sys, 'argv', ['run_tests.py', str(self.root), *args]):
            status = run_tests.main()
            return status, runner.call_args_list

    def test_default_only_runs_released(self):
        status, calls = self.invoke()
        self.assertEqual(status, 0)
        self.assertEqual([call.args[1] for call in calls], ['lab01_example'])

    def test_explicit_unreleased_preview(self):
        status, calls = self.invoke('--lab', 'lab02_example', '--include-unreleased')
        self.assertEqual(status, 0)
        self.assertEqual([call.args[1] for call in calls], ['lab02_example'])
        self.assertEqual(calls[0].kwargs['stage'], 'lab02_example')

    def test_cumulative_preview(self):
        status, calls = self.invoke('--through', 'lab02_example', '--include-unreleased')
        self.assertEqual(status, 0)
        self.assertEqual([call.args[1] for call in calls], ['lab01_example','lab02_example'])

    def test_unreleased_is_rejected_by_default(self):
        with self.assertRaises(SystemExit) as raised:
            self.invoke('--lab', 'lab02_example')
        self.assertEqual(raised.exception.code, 2)

    def test_empty_catalog_is_rejected(self):
        (self.root / 'lab_branches.json').write_text('{}')
        status, calls = self.invoke('--include-unreleased')
        self.assertEqual(status, 2)
        self.assertEqual(calls, [])

    def test_matrix_job_preserves_latest_released_stage(self):
        with patch.object(run_tests, 'released_labs', return_value=['lab01_example','lab02_example']), \
             patch.object(run_tests, 'run_lab', return_value=0) as runner, \
             patch.object(sys, 'argv', ['run_tests.py', str(self.root), '--lab', 'lab01_example']):
            self.assertEqual(run_tests.main(), 0)
            self.assertEqual(runner.call_args.kwargs['stage'], 'lab02_example')
