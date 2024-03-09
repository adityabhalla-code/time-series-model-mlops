FROM python:3.10.0-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required for compiling Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        python3-dev \
        libssl-dev \
        libffi-dev \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install Cython and numpy first to ensure their availability for pystan
RUN pip install cython numpy

# Then, install pystan
RUN pip install pystan==2.19.1.1

# After successfully installing pystan, install other dependencies
#RUN pip install pandas==1.2.1
#RUN pip install convertdate lunarcalendar holidays prophet==1.0.1

# Copy the Python dependencies file and the rest of  application's code into the container
COPY ./time_series_model_api/requirements.txt .
# copy the .whl file BEFORE attempting to install it with pip
COPY ./time_series_model_api/time_series_model-0.0.1-py3-none-any.whl .

RUN pip install -r requirements.txt

COPY ./time_series_model_api .

# Expose the port your app runs on
EXPOSE 8000

# start fastapi application
CMD ["python", "app/main.py"]