"""Enumerate knowledge inputs without silently swallowing directory errors."""
import os
from pathlib import Path


DEFAULT_LAYERS = ("general", "personal", "current")


def knowledge_dirs(root, layers, *, explicit=False):
    if not explicit:
        # Listing also checks that the root is readable. Absent default layers
        # are optional, but existing entries (including broken links) are not.
        configured = {entry.name for entry in root.iterdir()}
        layers = [layer for layer in layers if layer in configured]
        if not layers:
            raise FileNotFoundError(f"no configured knowledge layers in {root}")
    for layer in layers:
        yield root / layer / "knowledge"


def raise_walk_error(error):
    raise error


def markdown_files(root):
    for directory, subdirs, files in os.walk(root, onerror=raise_walk_error):
        subdirs[:] = [name for name in subdirs if name != ".git"]
        for name in files:
            if name.endswith(".md"):
                yield Path(directory) / name
