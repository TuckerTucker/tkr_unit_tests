import yaml
import json
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")

logger = logging.getLogger(__name__)

def load_config(config_file: str) -> Dict:
    """
    Loads the configuration from a YAML or JSON file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The loaded configuration.
    """
    try:
        with open(config_file, "r") as file:
            if config_file.endswith(".yaml") or config_file.endswith(".yml"):
                return yaml.safe_load(file)
            else:
                return json.load(file)
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {config_file}")
        raise
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        logger.error(f"Error loading configuration file: {e}")
        raise