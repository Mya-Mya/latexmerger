from .utils import *
from typing import Tuple, List, Optional
import re
from abc import ABC, abstractmethod

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
