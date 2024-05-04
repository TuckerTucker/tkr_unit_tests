import shutil
import logging
from pathlib import Path
from pathmanager import PathManager

logger = logging.getLogger(__name__)

def copy_file(src_path: Path, dst_path: Path, path_manager: PathManager) -> None:
    """
    Copies a file from the source path to the destination path.
    Args:
        src_path (Path): The source file path.
        dst_path (Path): The destination file path.
        path_manager (PathManager): An instance of the PathManager class.

    Raises:
        FileNotFoundError: If the source file is not found.
        shutil.SameFileError: If the source and destination files are the same.
        PermissionError: If there is insufficient permission to copy the file.
        OSError: If an error occurs during the file copy operation.
    """
    try:
        src_path = path_manager.resolve_path(src_path)
        dst_path = path_manager.resolve_path(dst_path)
        
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