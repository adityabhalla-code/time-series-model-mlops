# time-series-model-mlops
mlops for time series model using fb prophet
## Step 0: create python virtual env to run the repo
```python
python -m venv venv
pip install -r requirements.txt
# set up a jupyter kernel 
python -m ipkernel --name <env-name> --user
```
## Step 1: Develop the time series model in a jupyter environment
> refer the notebooks directory
## Step 2: Develop the repository for model training and prediction
> refer time_series_model directory
```python
# to train the model 
python time_series_model/train_pipeline.py
# for prediction
python time_series_model/predict.py
```
## Step 3: Develop a wheel package for model repository
> add files like pyproject.toml , manifest.in , mypy.in , setup.py
```python
python -m build
```

## Step 4:  Develop a fast api model 
> refere time_series_model_api directory
```python
# use below command to run the uvicorn server 
cd time_series_model_api
uvicorn main:app
```
## Step 5: 