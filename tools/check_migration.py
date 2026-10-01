"""Validate the migration inventory; optional argument checks the Java checkout."""

import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "docs/migration-manifest.json").read_text())
    entries = manifest["files"]
    names = [entry["source"] for entry in entries]
    if len(names) != manifest["source_count"] or len(set(names)) != len(names):
        raise ValueError("Duplicate or missing inventory entries")
    for entry in entries:
        if entry["status"] not in {"migrated", "replaced", "native", "documented"}:
            raise ValueError(f"Unresolved entry: {entry['source']}")
        for target in entry["targets"]:
            module, symbol = target.split(":")
            getattr(importlib.import_module("ultracomplexmath." + module), symbol)
        for test in entry["tests"]:
            if not (root / test).is_file():
                raise FileNotFoundError(test)
    if len(sys.argv) > 1:
        legacy = Path(sys.argv[1]).resolve()
        commit = subprocess.check_output(
            ["git", "-C", str(legacy), "rev-parse", "HEAD"], text=True
        ).strip()
        if commit != manifest["source_commit"]:
            raise ValueError("Java checkout is not the recorded baseline")
        actual = {str(path.relative_to(legacy)) for path in (legacy / "src").rglob("*.java")}
        if actual != set(names):
            raise ValueError(f"Java inventory differs: {actual ^ set(names)}")
        for entry in entries:
            digest = hashlib.sha256((legacy / entry["source"]).read_bytes()).hexdigest()
            if digest != entry["sha256"]:
                raise ValueError(f"Source changed: {entry['source']}")
        tracked = set(
            subprocess.check_output(["git", "-C", str(legacy), "ls-files"], text=True).splitlines()
        )
        if tracked != set(names) | set(manifest["ancillary_files"]):
            raise ValueError("Unaccounted repository files")
    print(f"{len(entries)} Java sources accounted for; targets and regression files exist.")


if __name__ == "__main__":
    main()
