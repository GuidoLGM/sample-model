import os
import yaml
from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
from box.exceptions import BoxValueError


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads yaml file and returns

    Args:
        path_to_yaml (Path): Path to yaml file

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox object
    """

    try:

        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError("empty file") from e
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list):
    """
    Create list of directories

    Args:
        path_to_directories (list): list of directories
        verbose (bool, optional): [description]. Defaults to True.
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
