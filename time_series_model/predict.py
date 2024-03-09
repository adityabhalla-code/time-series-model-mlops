import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import Union
import pandas as pd
import numpy as np

from time_series_model import __version__ as _version
from time_series_model.config.core import config
from time_series_model.processing.data_manager import load_pipeline
from time_series_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
time_series_pipe = load_pipeline(file_name=pipeline_file_name)

def make_predictions(*,input_data:Union[pd.DataFrame,dict])->dict:
    validated_data , errors = validate_inputs(input_df=pd.DataFrame(input_data))