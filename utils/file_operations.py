import json

import logging

logger = logging.getLogger(__name__)

def save_json(json_content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_content, f, ensure_ascii=False, indent=1)
    logger.info(f"Created {file_path}")


def save_csv(df, file_path):
    df.to_csv(file_path)
    logger.info(f"Created {file_path}")

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    logger.info(f"Loaded {len(content)} elements from {file_path}")
    return content


def save_to_file(data, file_path):
    """
    Salva i dati su un file JSON.
    """
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file)
    logger.info(f"Created {file_path}")

def load_from_file(file_path):
    """
    Carica i dati da un file JSON.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data
