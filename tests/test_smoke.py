"""Smoke tests: every module imports and the entry point answers --help."""

import importlib
import subprocess
import sys
import unittest

MODULES = ["parser", "algebra", "operations", "plotting", "diagnostics", "store", "service"]


class ModuleImportTests(unittest.TestCase):
    pass


def _make(name):
    def test(self):
        module = importlib.import_module("algebra_notebook." + name)
        self.assertTrue(module.__doc__)
    return test


for _name in MODULES:
    setattr(ModuleImportTests, "test_import_" + _name, _make(_name))


class EntryPointTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "algebra_notebook", *args],
                              capture_output=True, text=True, timeout=30)

    def test_help_names_the_options(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--data-dir", result.stdout)
        self.assertIn("--port", result.stdout)

    def test_start_is_not_implemented_yet(self):
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not implemented yet: see #14", result.stderr)


if __name__ == "__main__":
    unittest.main()
