from dataclasses import dataclass
import json
from pathlib import Path
import yaml
import os
from ensure import ensure_annotations
from box import ConfigBox

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    with open(path_to_yaml, 'r') as yaml_file:
        content = yaml.safe_load(yaml_file)
    return ConfigBox(content)

@ensure_annotations
def create_directories(path_to_directories: list,verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            print(f"Directory created: {path}")

@ensure_annotations
def get_size(path: Path) -> str:
    size_in_bytes = os.path.getsize(path)
    size_in_kb = size_in_bytes / 1024
    size_in_mb = size_in_kb / 1024
    return f"{size_in_mb:.2f} MB"

@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    with open(path,'r') as json_file:
        content=json.load(json_file)
    return ConfigBox(content)