"""Validate the pre-test lock; never reads benchmark answers."""
import hashlib
import json

from .day6_retriever import ROOT


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_selection():
    path = ROOT / "benchmark/selection_lock.json"
    if not path.exists():
        raise ValueError("Create benchmark/selection_lock.json before test evaluation")
    lock = json.loads(path.read_text(encoding="utf-8"))
    for relative, expected in lock["frozen_files_sha256"].items():
        if file_hash(ROOT / relative) != expected:
            raise ValueError(f"Frozen file changed after selection: {relative}")
    return lock
