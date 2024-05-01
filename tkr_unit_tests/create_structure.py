import os
import logging
from pathlib import Path
import configparser
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def read_gitignore(gitignore_path: str) -> set:
    """
    Reads the .gitignore file and returns a set of ignored paths.

    Args:
        gitignore_path (str): The path to the .gitignore file.

    Returns:
        set: A set of ignored paths.
    """
    ignored_paths = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored_paths.add(line)
    return ignored_paths

def read_tests_skip(tests_skip_path: str) -> set:
    """
    Reads the tests_skip.txt file and returns a set of paths to skip.

    Args:
        tests_skip_path (str): The path to the tests_skip.txt file.

    Returns:
        set: A set of paths to skip.
    """
    skip_paths = set()
    if os.path.exists(tests_skip_path):
        with open(tests_skip_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    skip_paths.add(line)
    return skip_paths

def read_gitmodules(gitmodules_path: str) -> set:
    """
    Reads the .gitmodules file and returns a set of submodule paths.

    Args:
        gitmodules_path (str): The path to the .gitmodules file.

    Returns:
        set: A set of submodule paths.
    """
    submodule_paths = set()
    if os.path.exists(gitmodules_path):
        config = configparser.ConfigParser()
        config.read(gitmodules_path)
        for section in config.sections():
            if "path" in config[section]:
                submodule_paths.add(config[section]["path"])
    return submodule_paths

def is_ignored(path: Path, ignored_paths: set) -> bool:
    """
    Checks if a given path should be ignored based on the ignored paths set.

    Args:
        path (Path): The path to check.
        ignored_paths (set): A set of ignored paths.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    for ignored_path in ignored_paths:
        if path.match(ignored_path):
            return True
    return False

def create_coveragerc(ignored_paths: set, coveragerc_path: str = ".coveragerc") -> None:
    """
    Creates the .coveragerc file based on the ignored paths.

    Args:
        ignored_paths (set): A set of ignored paths.
        coveragerc_path (str, optional): The path to the .coveragerc file. Defaults to ".coveragerc".
    """
    with open(coveragerc_path, "w") as file:
        file.write("[run]\n")
        file.write("omit =\n")
        for ignored_path in ignored_paths:
            file.write(f"    {ignored_path}\n")
    logger.info(f"Created .coveragerc file: {coveragerc_path}")

def create_test_structure(test_dir: str, gitignore_path: str = ".gitignore", tests_skip_path: str = "data/tests_skip.txt", gitmodules_path: str = ".gitmodules", coveragerc_path: str = ".coveragerc") -> None:
    """    
    Args:
        test_dir (str): The path to the test directory.
        gitignore_path (str, optional): The path to the .gitignore file. Defaults to ".gitignore".
        tests_skip_path (str, optional): The path to the tests_skip.txt file. Defaults to "tests_skip.txt".
        gitmodules_path (str, optional): The path to the .gitmodules file. Defaults to ".gitmodules".
        coveragerc_path (str, optional): The path to the .coveragerc file. Defaults to ".coveragerc".
    """
    logger.info("Creating test structure for the current working directory.")
    
    # Create the _reports directory within the test directory
    reports_dir = Path(test_dir) / "_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy the index.html file from the package to the _reports directory
    package_dir = Path(__file__).resolve().parent
    index_html_src = package_dir / "data/index.html"
    index_html_dst = reports_dir / "data/index.html"
    shutil.copy(index_html_src, index_html_dst)

    # Copy the pytest.ini file from the package to the parent directory
    pytest_ini_src = package_dir / "data/pytest.ini"
    pytest_ini_dst = Path.cwd() / "pytest.ini"
    shutil.copy(pytest_ini_src, pytest_ini_dst)
    
    # Read the .gitignore file
    ignored_paths = read_gitignore(gitignore_path)
    
    # Read the tests_skip.txt file
    skip_paths = read_tests_skip(tests_skip_path)
    ignored_paths.update(skip_paths)
    
    # Read the .gitmodules file
    submodule_paths = read_gitmodules(gitmodules_path)
    ignored_paths.update(submodule_paths)
    
    # Add the test_dir to the ignored paths
    ignored_paths.add(test_dir)
    
    # Create the .coveragerc file based on the ignored paths
    create_coveragerc(ignored_paths, coveragerc_path)
    
    # Walk through the current working directory
    for root, dirs, files in os.walk("."):
        root_path = Path(root)
        
        # Skip .git folders and directories specified in .gitignore, tests_skip.txt, and .gitmodules
        dirs[:] = filter(lambda d: d != ".git" and not is_ignored(root_path / d, ignored_paths), dirs)
        
        # Skip files specified in .gitignore, tests_skip.txt, and the file running the create_test_structure
        files = filter(lambda f: not is_ignored(root_path / f, ignored_paths) and f != os.path.basename(__file__), files)
        
        # Skip empty directories
        if not dirs and not files:
            logger.info(f"Skipping empty directory: {root}")
            continue
        
        # Create the corresponding test directory
        test_path = Path(test_dir) / root
        test_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created test directory: {test_path}")
        
        # Create __init__.py file in the test directory if it doesn't exist
        init_file_path = test_path / "__init__.py"
        init_file_path.touch(exist_ok=True)
        logger.info(f"Created __init__.py file: {init_file_path}")
        
        # Create empty test files for each Python file in the package if they don't exist
        test_files = [f"test_{file}" for file in files if file.endswith(".py")]
        list(map(lambda test_file: (test_path / test_file).touch(exist_ok=True), test_files))
        logger.info(f"Created test files: {', '.join(str(test_path / test_file) for test_file in test_files)}")
    
    logger.info("Test structure creation completed.")