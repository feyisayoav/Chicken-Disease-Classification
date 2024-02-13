import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads YAML file and returns
    Args:
        path_to_yaml (Path): Path like input
    Raises:
        ValueErro: If yaml file not found
        e: empty file
    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create directories
   Args:
       path_to_directories (list): list of path of directories
       ignore_log (bool, optional): ignore if multiple directories are passed. Defaults to False.
        """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
           logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves data in json format
    Args:
        path (Path): path to json file
        data (dict): data to be saved in json format
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")
    
@ensure_annotations
def load_json(path: Path) -> Any:
    """
    Loads json file
    Args:
        path (Path): path to json file
    Returns:
        ConfigBox: data as class attributes instead of dictionary
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves data in binary format
    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")
    
@ensure_annotations
def load_bin(path: Path) -> Any:
    """ Loads binary file
    Args:
        path (Path): path to binary file
    Returns:
        Any: Object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded succesfully from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Gets file size
    Args:
        path (Path): path of the file
    Returns:
        str: file size in kb
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"{size_in_kb} KB"

def decodeImage(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedimagepath):
    with open(croppedimagepath, "rb") as f:
        return base64.b64encode(f.read())
