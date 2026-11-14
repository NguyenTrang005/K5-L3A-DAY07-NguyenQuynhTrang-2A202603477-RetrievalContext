import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from src.selection import file_hash, load_selection


class SelectionTests(unittest.TestCase):
    def test_lock_requires_unchanged_pipeline_and_benchmark(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "benchmark").mkdir()
            source = root / "pipeline.py"
            source.write_text("original", encoding="utf-8")
            lock = {"frozen_files_sha256": {"pipeline.py": file_hash(source)}}
            (root / "benchmark/selection_lock.json").write_text(json.dumps(lock), encoding="utf-8")
            with patch("src.selection.ROOT", root):
                self.assertEqual(load_selection(), lock)
                source.write_text("changed", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Frozen file changed"):
                    load_selection()

    def test_no_test_without_lock(self):
        with TemporaryDirectory() as tmp:
            with patch("src.selection.ROOT", Path(tmp)):
                with self.assertRaisesRegex(ValueError, "before test"):
                    load_selection()
