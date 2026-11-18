"""Starter structural checks only; add tests for the actual product behavior."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StructureTests(unittest.TestCase):
    def test_plugin_identity_and_skill_entrypoint(self):
        portable = json.loads((ROOT / 'plugin.json').read_text())
        self.assertTrue(portable['version'])
        self.assertTrue(list((ROOT / 'skills').glob('*/SKILL.md')))
