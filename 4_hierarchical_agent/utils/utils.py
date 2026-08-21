# Copyright (c) 2024 Maggie Mhanna
# All rights reserved.

import os
import yaml
from pathlib import Path

from utils.logging import setup_logging

# --- Configuration & Setup ---
logger = setup_logging(name=__name__)

def load_env_variables(file_path: Path) -> None:
    """Reads a YAML file and sets the key-value pairs as environment variables."""
    if not file_path.exists():
        logger.error(f"Environment file not found: {file_path}")
        return

    try:
        with file_path.open('r') as file:
            env_vars = yaml.safe_load(file) or {}
            for key, value in env_vars.items():
                os.environ[key] = str(value) 
                logger.info(f"Loaded {key} into environment.")
    except Exception as e:
        logger.error(f"Error loading environment variables from {file_path}: {e}")