"""
YAML configuration management utilities
"""
from pathlib import Path
from typing import Dict, Any
import shutil
import yaml


def read_yaml_config(config_path: Path) -> Dict[str, Any]:
    """
    Read YAML configuration file
    
    Args:
        config_path: Path to the YAML file
    
    Returns:
        Configuration dictionary or error dict if not found
    """
    if not config_path.exists():
        return {"error": "Configuration not found"}
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def update_yaml_config(config_path: Path, config: Dict[str, Any]) -> bool:
    """
    Update YAML configuration file with backup
    
    Args:
        config_path: Path to the YAML file
        config: New configuration dictionary
    
    Returns:
        True if successful, raises exception on error
    """
    # Backup existing config
    backup_path = config_path.with_suffix('.yaml.bak')
    if config_path.exists():
        shutil.copy(config_path, backup_path)
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        # Restore backup on error
        if backup_path.exists():
            shutil.copy(backup_path, config_path)
        raise e