"""Check all suite metadata without needing a student implementation."""
import json
from pathlib import Path
import re
import unittest
from run_tests import released_labs

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def test_catalog_covers_all_ten_labs_in_order(self):
        catalog = json.loads((ROOT / 'lab_branches.json').read_text())
        self.assertEqual([key[:5] for key in catalog], [f'lab{n:02}' for n in range(1, 11)])
        for lab, branch in catalog.items():
            self.assertRegex(lab, r'^lab[0-9]{2}_[a-z0-9_]+$')
            self.assertIsInstance(branch, str)
            self.assertTrue(list((ROOT / lab).glob('test_*.py')))

    def test_release_is_ordered_catalog_subset(self):
        catalog = list(json.loads((ROOT / 'lab_branches.json').read_text()))
        selected = released_labs()
        self.assertEqual(selected, [lab for lab in catalog if lab in selected])

    def test_all_program_cases_have_valid_expectations(self):
        files = list(ROOT.glob('lab*/cases.json'))
        self.assertEqual(len(files), 6)
        for path in files:
            cases = json.loads(path.read_text())
            self.assertTrue(cases)
            names = []
            for case in cases:
                with self.subTest(lab=path.parent.name, name=case.get('name')):
                    self.assertRegex(case['name'], r'^[a-z][a-z0-9_]+$')
                    names.append(case['name'])
                    self.assertIsInstance(case['source'], str)
                    self.assertTrue(case['requirement'])
                    self.assertEqual(sum(key in case for key in ('output','error','clock')), 1)
                    if 'output' in case:
                        self.assertIsInstance(case['output'], list)
                    if 'error' in case:
                        re.compile(case['error'])
                    if 'clock' in case:
                        self.assertIs(case['clock'], True)
            self.assertEqual(len(names), len(set(names)))
