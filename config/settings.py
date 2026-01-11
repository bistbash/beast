"""
Global Settings
Configuration for the entire system
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# School information
SCHOOL_NAME = "טכני באר שבע"
PROJECT_NAME = "BEAST"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///beast.db")

# Configuration paths
CONFIG_DIR = BASE_DIR / "config"
HIERARCHY_CONFIG_PATH = CONFIG_DIR / "hierarchy.yaml"

# Department configuration
DEPARTMENTS_CONFIG_PATH = CONFIG_DIR / "departments.yaml"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"

# Create necessary directories
LOG_DIR.mkdir(exist_ok=True)
