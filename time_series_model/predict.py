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
    predictions = time_series_pipe.predict(validated_data)
    results = {"predictions": predictions['yhat'].values,"version": _version, "errors": errors}
    print(f"Results---\n{results}")
    if not errors:
        predictions = time_series_pipe.predict(validated_data)
        results = {"predictions": predictions['yhat'].values, "version": _version, "errors": errors}
    return results

if __name__ == "__main__":

    data_in = {
        "ds":['202307','202308'],
        "RBOB_Gasoline_t_2": [3.39,4.39],
        "US_Corn_t_1": [687.50 ,699.50],
        "US_Cocoa_t_2": [2437,2500],
        "consumption_t_1": [790.10,799.10],
        "Ind_Prod_t_1": [100.50,101.50],
        "Unit_labor_t_1": [125.57,130]
    }
    make_predictions(input_data=data_in)


