# Path setup and access the config.yml

import sys
from pathlib import Path

file = Path(__file__).resolve()
parent , root = file.parent , file.parents[1]
sys.path.append(str(root))

from typing import List
from pydantic import BaseModel , validator
from strictyaml import YAML , load

import time_series_model
PACKAGE_ROOT = Path(time_series_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT/"trained_models"

class AppConfig(BaseModel):
    """
    Application-level confi.
    """
    package_name : str
    training_data_file : str
    test_data_file : str
    pipeline_save_file : str

class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering
    """
    target : str
    features : List[str]
    date_var : str
    growth : str
    daily_seasonality : bool
    seasonality_mode : str
    changepoint_prior_scale : float
    seasonality_prior_Scale : float
    seasonality_name : str
    seasonality_period : int
    fourier_order : int
    regressor_1 : str
    regressor_2 : str
    regressor_3 : str

class Config(BaseModel):
    """
    Master config object
    """
    app_config : AppConfig
    model_config : ModelConfig

def find_config_file() -> Path:
    """
    Locate the configuration file
    """
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")

def fetch_config_from_yaml(cfg_path:Path=None)-> YAML:
    """Parse YAML  containing the package configuration"""
    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path,'r') as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path:{cfg_path}")

def create_and_validate_cofig(parsed_config:YAML=None)->Config:
    """Run validation on cofig values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from strictyaml YAML type
    _config = Config(
        app_config = AppConfig(**parsed_config.data),
        model_config = ModelConfig(**parsed_config.data)
    )
    print(_config)
    return _config

config = create_and_validate_cofig()