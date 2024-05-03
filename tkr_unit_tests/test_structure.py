import yaml
import os
import logging
from pathlib import Path
import json
from typing import Dict, Set
from config import load_config
from file_utils import read_ignore_file, is_ignored_path, copy_file

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_coveragerc(ignored_paths: Set[str]) -> None:
    """
    Creates the .coveragerc file based on the ignored paths.

    Args:
        ignored_paths (Set[str]): A set of ignored paths.
    """
    try:
        with open(".coveragerc", "w") as file:
            file.write("[run]\n")
            file.write("omit =\n")
            for ignored_path in ignored_paths:
                file.write(f"    {ignored_path}\n")
        logger.info("Created .coveragerc file")
    except OSError as e:
        logger.error(f"Error creating .coveragerc file: {e}")
        raise

def create_test_files(test_path: Path, module_file: str, project_dir: Path) -> None:
    """
    Creates a test file for a given module file.

    Args:
        test_path (Path): The path to the test directory.
        module_file (str): The name of the module file.
        project_dir (Path): The path to the project directory.
    """
    if module_file.endswith(".py"):
        test_file_name = f"test_{module_file}"
        test_file_path = test_path / test_file_name

        # Write a basic test template to the test file if it doesn't exist
        if not test_file_path.exists():
            module_name = module_file[:-3]
            test_template = f"""import unittest
from {test_path.relative_to(project_dir).as_posix().replace('/', '.')}.{module_name} import *

class Test{module_name.capitalize()}(unittest.TestCase):
    def test_{module_name}(self):
        # TODO: Implement test case
        pass

if __name__ == '__main__':
    unittest.main()
"""
            try:
                test_file_path.write_text(test_template.strip())
                logger.info(f"Created test file: {test_file_path}")
            except OSError as e:
                logger.error(f"Error creating test file {test_file_path}: {e}")
                raise

def create_structure(config_file: str) -> None:
    """
    Creates the test structure for the project based on the configuration file.

    Args:
        config_file (str): The path to the configuration file (YAML or JSON).
    """
    try:
        config = load_config(config_file)
    except (FileNotFoundError, json.JSONDecodeError, yaml.YAMLError) as e:
        logger.error(f"Error loading configuration file: {e}")
        raise

    # Validate the configuration file
    required_fields = ["project_dir", "test_dir", "ignore_files", "package_data_dir", "module_paths_file"]
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required field in configuration file: {field}")
            raise ValueError(f"Invalid configuration file: Missing field '{field}'")

    project_dir = Path(config["project_dir"]).absolute()
    test_dir = config["test_dir"]
    ignore_files = [project_dir / file for file in config["ignore_files"]]
    package_data_dir = Path(config["package_data_dir"]).absolute()
    module_paths_file = config["module_paths_file"]

    logger.info(f"Creating test structure for the project: {project_dir}")

    # Read the ignore files and combine the ignored paths
    ignored_paths = set()
    for ignore_file in ignore_files:
        try:
            ignored_paths.update(read_ignore_file(ignore_file))
        except FileNotFoundError as e:
            logger.warning(f"Ignore file not found: {ignore_file}. Skipping.")

    # Add the test directory to the ignored paths
    ignored_paths.add(test_dir)

    # Add .git folders to the ignored paths
    ignored_paths.add(".git")

    # Create the .coveragerc file based on the ignored paths
    try:
        create_coveragerc(ignored_paths)
    except OSError as e:
        logger.error(f"Error creating .coveragerc file: {e}")
        raise

    # Copy the pytest.ini file from the package data directory to the project directory
    try:
        copy_file(package_data_dir / "pytest.ini", project_dir / "pytest.ini")
    except FileNotFoundError as e:
        logger.warning(f"pytest.ini file not found in package data directory. Skipping.")
    except OSError as e:
        logger.error(f"Error copying pytest.ini file: {e}")
        raise

    # Create the _reports directory within the test directory
    reports_dir = project_dir / test_dir / "_reports"
    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Error creating _reports directory: {e}")
        raise

    # Copy the index.html file from the package data directory to the _reports directory
    try:
        copy_file(package_data_dir / "index.html", reports_dir / "index.html")
    except FileNotFoundError as e:
        logger.warning(f"index.html file not found in package data directory. Skipping.")
    except OSError as e:
        logger.error(f"Error copying index.html file: {e}")
        raise

    # Initialize a dictionary to store module paths
    module_paths: Dict[str, str] = {}

    # Read the tests_skip.txt file to get the list of skipped modules and directories
    tests_skip_file = project_dir / "tests_skip.txt"
    skipped_paths = set()
    if tests_skip_file.exists():
        with open(tests_skip_file, "r") as file:
            skipped_paths = set(line.strip() for line in file)

    # Walk through the project directory
    for root, dirs, files in os.walk(project_dir):
        root_path = Path(root).absolute()

        # Skip ignored directories
        dirs[:] = [d for d in dirs if not is_ignored_path(root_path / d, ignored_paths, __file__)]

        # Skip skipped directories
        dirs[:] = [d for d in dirs if str(root_path / d) not in skipped_paths]

        # Skip ignored files
        files = [f for f in files if not is_ignored_path(root_path / f, ignored_paths, __file__)]

        # Skip empty directories
        if not dirs and not files:
            logger.info(f"Skipping empty directory: {root_path}")
            continue

        # Create the corresponding test directory
        test_path = project_dir / test_dir / root_path.relative_to(project_dir)
        try:
            test_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created test directory: {test_path}")
        except OSError as e:
            logger.error(f"Error creating test directory {test_path}: {e}")
            raise

        # Create __init__.py file in the test directory if it doesn't exist
        init_file_path = test_path / "__init__.py"
        try:
            init_file_path.touch(exist_ok=True)
            logger.info(f"Created __init__.py file: {init_file_path}")
        except OSError as e:
            logger.error(f"Error creating __init__.py file {init_file_path}: {e}")
            raise

# Create test files for each Python file in the package
        for module_file in files:
            if module_file.endswith(".py"):  # Only process Python files
                module_path = root_path / module_file
                relative_module_path = str(module_path.relative_to(project_dir))

                # Skip skipped modules
                if relative_module_path in skipped_paths:
                    logger.info(f"Skipping module: {relative_module_path}")
                    continue

                try:
                    create_test_files(test_path, module_file, project_dir)
                except OSError as e:
                    logger.error(f"Error creating test file for module {module_file}: {e}")
                    raise

                # Store the module's full path in the dictionary
                module_paths[str(test_path / f"test_{module_file}")] = str(module_path)

    # Write the module paths to a JSON file in the project directory
    module_paths_file_path = project_dir / test_dir / module_paths_file
    try:
        with open(module_paths_file_path, "w") as file:
            json.dump(module_paths, file, indent=4)
        logger.info(f"Module paths stored in: {module_paths_file_path}")
    except OSError as e:
        logger.error(f"Error writing module paths to file {module_paths_file_path}: {e}")
        raise

    logger.info("Test structure creation completed.")