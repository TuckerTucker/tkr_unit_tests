import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def install_allure_commandline() -> None:
    """
    Installs Allure commandline globally using npm.
    """
    try:
        logger.info("Installing Allure commandline...")
        subprocess.run(["npm", "install", "-g", "allure-commandline"], check=True)
        logger.info("Allure commandline installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Allure commandline. Error: {str(e)}")
        sys.exit(1)

def main() -> None:
    """
    Main function to run the Allure commandline installation.
    """
    install_allure_commandline()

if __name__ == "__main__":
    main()