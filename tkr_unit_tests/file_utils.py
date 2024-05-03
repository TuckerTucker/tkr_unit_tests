import os
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def read_ignore_file(file_path: str) -> set:
    """
    Reads an ignore file and returns a set of ignored paths.

    Args:
        file_path (str): The path to the ignore file.

    Returns:
        set: A set of ignored paths.

    Raises:
        FileNotFoundError: If the ignore file is not found.
    """
    ignored_paths = set()
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored_paths.add(line)
    except FileNotFoundError as e:
        logger.error(f"Ignore file not found: {file_path}")
        raise e
    logger.info(f"Read ignore file: {file_path}")
    return ignored_paths

def is_ignored_path(path: Path, ignored_paths: set, current_file: str) -> bool:
    """
    Checks if a given path should be ignored.

    Args:
        path (Path): The path to check.
        ignored_paths (set): A set of ignored paths.
        current_file (str): The file running the create_structure function.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    is_ignored = any(path.match(ignored_path) for ignored_path in ignored_paths) or path.name == current_file
    logger.debug(f"Checking if path is ignored: {path} - Ignored: {is_ignored}")
    return is_ignored

def copy_file(src_path: Path, dst_path: Path) -> None:
    """
    Copies a file from the source path to the destination path.

    Args:
        src_path (Path): The source file path.
        dst_path (Path): The destination file path.

    Raises:
        FileNotFoundError: If the source file is not found.
        shutil.SameFileError: If the source and destination files are the same.
        PermissionError: If there is insufficient permission to copy the file.
        OSError: If an error occurs during the file copy operation.
    """
    try:
        shutil.copy(src_path, dst_path)
        logger.info(f"Copied file: {src_path} -> {dst_path}")
    except FileNotFoundError as e:
        logger.error(f"Source file not found: {src_path}")
        raise e
    except shutil.SameFileError as e:
        logger.error(f"Source and destination files are the same: {src_path}")
        raise e
    except PermissionError as e:
        logger.error(f"Insufficient permission to copy file: {src_path}")
        raise e
    except OSError as e:
        logger.error(f"Error occurred while copying file: {src_path}")
        raise e