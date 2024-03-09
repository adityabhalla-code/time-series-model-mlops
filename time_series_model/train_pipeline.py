import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from time_series_model.config.core import config
from time_series_model.pipeline import timeSeriesPipeline
from time_series_model.processing.data_manager import load_dataset, save_pipeline

def run_training()-> None:
    data = load_dataset(file_name=config.app_config.training_data_file)
    # Fit the pipeline
    # train_data = data.drop('y',axis=1)
    # print(train_data.info())
    # print(data['y'])
    timeSeriesPipeline.fit(data)
    print("------pipeline has been fitted------------")
    # Create the future dates DataFrame
    future = timeSeriesPipeline.named_steps['prophet'].make_future_dataframe(periods=6, freq='M')
    print("------Future data to test the model--------")
    print(future)
    # Predict on the future dates
    forecast = timeSeriesPipeline.predict(future)
    # Check the last few forecasted values
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    # Evaluation Metrics for Fbprophet
    y_true = data['y'][-5:].values
    y_pred = forecast['yhat'][-5:].values
    mae_prophet = mean_absolute_error(y_true, y_pred)
    rmse_prophet = np.sqrt(mean_squared_error(y_true, y_pred))
    mape_prophet = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    print(f"Mean Absolute Error <prophet>--{mae_prophet}")
    print(f"Root Mean Square Error <prophet>--{rmse_prophet}")
    print(f"Mean Absolute Percentage Error <prophet>--{mape_prophet}")
    # persist trained model
    save_pipeline(pipeline_to_persist=timeSeriesPipeline)


if __name__ == "__main__":
    run_training()
