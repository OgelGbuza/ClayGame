# data_loader.py
"""
A simple data loader that reads external JSON files for dialogue, quests, levels, etc.
"""
import json, os, logging

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join("assets", "data")

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        logger.warning(f"Data file {filepath} not found. Returning empty dict.")
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Loaded data from {filename}")
            return data
    except Exception as e:
        logger.error(f"Error reading {filename}: {e}")
        return {}
