from typing import Tuple, List, Optional
from argparse import ArgumentParser
from pathlib import Path
import re
from abc import ABC, abstractmethod

root: Path = None


def parse_args() -> Tuple[Path, Path, Path]:
    parser = ArgumentParser(
        prog="texpack", description="Pack LaTeX Files into Single .tex File"
    )
    parser.add_argument("entry", type=Path, help="Entry .tex File Path")
    parser.add_argument(
        "--output",
        "-o",
        required=False,
        type=str,
        help="Output .tex File Name",
        default=None,
    )
    parsed = parser.parse_args()
    entry = Path(parsed.entry)
    entry_fn = entry.name
    parent = entry.parent
    output = parsed.output or f"merged_{entry_fn}"
    output_fp = parent / output
    return entry, parent, output_fp


def read_text(f: Path) -> str:
    return f.read_text("utf-8")


class BodyExtractor(ABC):
    @abstractmethod
    def matches(self, line: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def extract(self, parent: Path, root: Path, line: str) -> Tuple[List[str], Path]:
        raise NotImplementedError()


class InputExtractor(BodyExtractor):
    def __init__(self) -> None:
        self.pat = re.compile(r"\\input\{(.*)\}")

    def matches(self, line: str) -> bool:
        return bool(self.pat.match(line))

    def extract(self, parent: Path, root: Path, line: str) -> Tuple[List[str], Path]:
        mat = self.pat.match(line)
        stem = mat.group(1)
        # The entry file's directory - based relative path is required for \input.
        target = root / f"{stem}.tex"
        body = read_text(target)
        body_lines = body.split("\n")
        return body_lines, target


class SubfileExtractor(BodyExtractor):
    def __init__(self) -> None:
        self.pat = re.compile(r"\\subfile\{(.*)\}")

    def matches(self, line: str) -> bool:
        return bool(self.pat.match(line))

    def extract(self, parent: Path, root: Path, line: str) -> Tuple[List[str], Path]:
        mat = self.pat.match(line)
        stem = mat.group(1)
        target = parent / f"{stem}.tex"
        text = read_text(target)
        lines = text.split("\n")
        body_lines = []

        in_body = False
        for line in lines:
            if line.startswith("\\begin{document}"):
                in_body = True
            elif line.endswith("\\end{document}"):
                in_body = False
            elif in_body:
                body_lines.append(line)

        return body_lines, target


extractors: List[BodyExtractor] = [InputExtractor(), SubfileExtractor()]


def extract_ifany(parent: Path, line: str) -> Optional[Tuple[List[str], Path]]:
    for extractor in extractors:
        if extractor.matches(line):
            return extractor.extract(parent, root, line)
    return None


def expand(parent: Path, lines: List[str], depth: int = 0) -> List[str]:
    expanded_lines = []

    for line in lines:
        extracted = extract_ifany(parent, line)
        if extracted is not None:
            body_lines, target = extracted
            arrow = ">" * (depth + 1)
            barrow = "<" * (depth + 1)
            target_relation = str(target.relative_to(root))
            expanded_lines.append(f"% {arrow} {target_relation} {arrow} : texpack")
            expanded_lines += expand(target.parent, body_lines, depth=depth + 1)
            expanded_lines.append(f"% {barrow} {target_relation} {barrow} : texpack")
        else:
            expanded_lines.append(line)
    return expanded_lines


def main():
    entry, parent, output_fp = parse_args()
    if output_fp.exists():
        response = input(
            f"The output file {output_fp.name} already exists. OVERWRITE THIS? ARE YOU SURE? [Y/other]"
        )
        if response != "Y":
            print("Aborted.")
            exit(-1)

    global root
    root = parent
    entry_lines = read_text(entry).split("\n")
    result = expand(parent, entry_lines)
    text = "\n".join(result)
    output_fp.write_text(text)
    print("Merged File Written.")


if __name__ == "__main__":
    main()
