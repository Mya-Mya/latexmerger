from pathlib import Path


def read_text(f: Path) -> str:
    return f.read_text("utf-8")
