from typing import Any , List , Optional, Dict
from pydantic import BaseModel
from time_series_model.processing.validation import DataInputSchema

class PredictionResults(BaseModel):
    errors : Optional[Dict]
    version : str
    predictions : List[float]


class MultipleDataInputs(BaseModel):
    inputs : List[DataInputSchema]

    class Config:
        schema_extra = {
            "example":{
                "inputs":[
                    {
                        "ds":'202307',
                        "RBOB_Gasoline_t_2": 3.39,
                        "US_Corn_t_1": 687.50,
                        "US_Cocoa_t_2": 2437.00,
                        "consumption_t_1": 790.10,
                        "Ind_Prod_t_1": 100.50,
                        "Unit_labor_t_1": 125.57
                    }
                ]
            }
        }