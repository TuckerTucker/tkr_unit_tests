import yaml
import os
import logging
from pathlib import Path
import json
from typing import Dict, Set
from config import load_config
from file_utils import copy_file
from pathmanager import PathManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_coveragerc(project_dir: Path, ignored_paths: Set[str]) -> None:
    """
    Creates the .coveragerc file based on the ignored paths in the project directory.

    Args:
        project_dir (Path): The path to the project directory.
        ignored_paths (Set[str]): A set of ignored paths.
    """
    try:
        coveragerc_path = project_dir / ".coveragerc"
        with open(coveragerc_path, "w") as file:
            file.write("[run]\n")
            file.write("omit =\n")
            for ignored_path in ignored_paths:
                file.write(f"    {ignored_path}\n")
        logger.info(f"Created .coveragerc file: {coveragerc_path}")
    except OSError as e:
        logger.error(f"Error creating .coveragerc file: {e}")
        raise

def create_test_files(test_path: Path, module_file: str, project_dir: Path, path_manager: PathManager) -> None:
    """
    Creates a test file for a given module file.

    Args:
        test_path (Path): The path to the test directory.
        module_file (str): The name of the module file.
        project_dir (Path): The path to the project directory.
        path_manager (PathManager): An instance of the PathManager class.
    """
    if module_file.endswith(".py"):
        test_file_name = f"test_{module_file}"
        test_file_path = test_path / test_file_name

        # Write a basic test template to the test file if it doesn't exist
        if not test_file_path.exists():
            module_name = module_file[:-3]
            test_template = f"""import unittest
            from {path_manager.resolve_path(test_path).relative_to(project_dir).as_posix().replace('/', '.')}.{module_name} import *

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

    # Create an instance of the PathManager class
    path_manager = PathManager(project_dir)

    # Read the ignore rules from the specified files
    ignore_patterns = path_manager.read_ignore_rules(ignore_files)

    # Add to the ignore patterns
    ignore_patterns.append(test_dir)
    ignore_patterns.append(".git")
    ignore_patterns.append("my_tests")
    ignore_patterns.append("module_paths.json")
    
    # Create the .coveragerc file based on the ignore patterns
    try:
        create_coveragerc(project_dir, ignore_patterns)
    except OSError as e:
        logger.error(f"Error creating .coveragerc file: {e}")
        raise

    # Copy the pytest.ini file from the package data directory to the project directory
    try:
        copy_file(package_data_dir / "pytest.ini", project_dir / "pytest.ini", path_manager)
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
        copy_file(package_data_dir / "index.html", reports_dir / "index.html", path_manager)
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

    # Copy test_*.py modules from my_tests to _tests
    my_tests_dir = project_dir / "my_tests"
    if my_tests_dir.exists():
        for test_file in my_tests_dir.glob("test_*.py"):
            try:
                copy_file(test_file, project_dir / test_dir / test_file.name, path_manager)
                logger.info(f"Copied test file: {test_file} -> {project_dir / test_dir / test_file.name}")
            except OSError as e:
                logger.error(f"Error copying test file {test_file}: {e}")
                raise
            
    # Walk through the project directory using the PathManager
    for file_path in path_manager.walk_directory(project_dir, ignore_patterns):
        if file_path.suffix == ".py":
            relative_path = file_path.relative_to(project_dir)
            test_path = project_dir / test_dir / relative_path.parent
            module_file = file_path.name

            try:
                create_test_files(test_path, module_file, project_dir, path_manager)
            except OSError as e:
                logger.error(f"Error creating test file for module {module_file}: {e}")
                raise

            module_paths[str(test_path / f"test_{module_file}")] = str(file_path)

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