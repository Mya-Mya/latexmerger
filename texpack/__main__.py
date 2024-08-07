from typing import Tuple, List, Optional
from argparse import ArgumentParser
from pathlib import Path
from .extractors import *
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
    output = parsed.output or f"texpack-{entry_fn}"
    output_fp = parent / output
    return entry, parent, output_fp



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
    print(f"Written to {str(output_fp)}.")


if __name__ == "__main__":
    main()
