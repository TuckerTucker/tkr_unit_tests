import argparse
import logging
from config import load_config
from test_structure import create_structure

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the test structure creation process...")

    parser = argparse.ArgumentParser(description="Create test structure for a project.")
    parser.add_argument("--project-dir", help="Root directory of the project", required=True)
    parser.add_argument("--test-dir", default="_tests", help="Name of the test directory (default: _tests)")
    parser.add_argument("--gitignore", default=".gitignore", help="Path to the .gitignore file (default: .gitignore)")
    parser.add_argument("--tests-skip", default="tests_skip.txt", help="Path to the tests_skip.txt file (default: tests_skip.txt)")
    args = parser.parse_args()

    logger.info(f"Command-line arguments: {args}")

    # Load the configuration file
    config_file = "config.yaml"
    try:
        config = load_config(config_file)
        logger.info(f"Loaded configuration from {config_file}: {config}")
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found.")
        raise
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        raise

    # Update the configuration with command-line arguments
    config["test_dir"] = args.test_dir
    config["ignore_files"] = [args.gitignore, args.tests_skip]
    logger.info(f"Updated configuration: {config}")

    # Create the test structure
    try:
        create_structure(config_file)
        logger.info("Test structure creation completed successfully.")
    except Exception as e:
        logger.error(f"Error creating test structure: {e}")
        raise

if __name__ == "__main__":
    main()