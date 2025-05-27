# utils/utils.py

import yaml
import os
import re
def read_yaml_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def save_code_to_file(code, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(code)
def extract_code(text: str) -> str | None:
    patterns = [
        # Standard markdown with python specified
        (r"```python\s*(.*?)\s*```", re.DOTALL),
        # Generic code block (any language or none)
        (r"```\s*(.*?)\s*```", re.DOTALL),
        # Non-standard single quote variants
        (r"'''python\s*(.*?)\s*'''", re.DOTALL),
        (r"'''\s*(.*?)\s*'''", re.DOTALL)
    ]
    
    for pattern, flags in patterns:
        match = re.search(pattern, text, flags)
        if match:
            code = match.group(1).strip()
            if code:
                return code
    return None