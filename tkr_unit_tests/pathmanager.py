import os
from pathlib import Path
import fnmatch
import logging
from typing import Iterator

logger = logging.getLogger(__name__)

class PathManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()

    def resolve_path(self, path: str) -> Path:
        """
        Resolves a relative path to an absolute path based on the base directory.

        Args:
            path (str): The path to resolve.

        Returns:
            Path: The resolved absolute path.
        """
        return (self.base_dir / path).resolve()

    def is_ignored(self, path: Path, ignore_patterns: list) -> bool:
        """
        Checks if a given path should be ignored based on the ignore patterns.

        Args:
            path (Path): The path to check.
            ignore_patterns (list): A list of ignore patterns.

        Returns:
            bool: True if the path should be ignored, False otherwise.
        """
        relative_path = path.relative_to(self.base_dir)
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(str(relative_path), pattern):
                logger.debug(f"Path {path} matches ignore pattern {pattern}")
                return True
        logger.debug(f"Path {path} does not match any ignore patterns")
        return False

    def read_ignore_rules(self, ignore_files: list) -> list:
        """
        Reads ignore rules from the specified files.

        Args:
            ignore_files (list): A list of file paths containing ignore rules.

        Returns:
            list: A list of ignore patterns.
        """
        ignore_patterns = []
        for ignore_file in ignore_files:
            try:
                with open(ignore_file, "r") as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            ignore_patterns.append(line)
            except FileNotFoundError:
                logger.warning(f"Ignore file not found: {ignore_file}")
        return ignore_patterns

    def walk_directory(self, directory: Path, ignore_patterns: list) -> Iterator[Path]:
        """
        Recursively walks through a directory and its subdirectories, yielding each file path.

        Args:
            directory (Path): The directory to walk through.
            ignore_patterns (list): A list of ignore patterns.

        Yields:
            Path: The path of each file encountered during the directory walk.
        """
        for item in directory.iterdir():
            if self.is_ignored(item, ignore_patterns):
                logger.debug(f"Ignoring path: {item}")
                continue

            if item.is_dir():
                yield from self.walk_directory(item, ignore_patterns)
            else:
                yield item