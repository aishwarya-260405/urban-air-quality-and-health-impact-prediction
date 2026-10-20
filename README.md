# Urban Air Quality & Health Impact Prediction

## Overview

Urban Air Quality & Health Impact Prediction is an end-to-end data-driven framework designed to forecast next-day AQI and provide personalized health risk information using air quality, weather, and user health-profile data from Chennai.

The system integrates historical data preprocessing and model development with live air quality data acquisition, real-time AQI forecasting, and personalized health assessment through a Flask-based web application.

## Key Components

### Data Preprocessing

- Integrated historical air quality and meteorological datasets.
- Handled missing values and maintained consistent feature formats.
- Created lag-based AQI features and rolling averages.
- Used a chronological train-validation-test split to preserve temporal order and avoid data leakage.

### Forecasting Models

The forecasting approaches evaluated in the project include:

- Naive Persistence
- ARIMA
- Random Forest
- XGBoost
- Artificial Neural Network (ANN)
- Long Short-Term Memory (LSTM)

The models were evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- R² Score

ARIMA achieved the lowest MAE and highest R² Score in the model comparison, while Random Forest demonstrated comparable forecasting performance. Random Forest was selected for the real-time deployment pipeline.

### Real-Time AQI Forecasting

The deployed forecasting pipeline uses a trained Random Forest Regressor to predict next-day AQI.

The live prediction pipeline uses a rolling 30-day history and generates features including:

- Current AQI
- AQI lag features
- 3-day rolling AQI
- 7-day rolling AQI
- Temperature
- Humidity
- Wind speed
- Wind direction
- Atmospheric pressure
- Rainfall
- Calendar features
- Monitoring-station indicators

### Personalized Health Risk Assessment

The system combines AQI information with user-specific factors such as:

- Age
- Existing health conditions
- Smoking status

It generates personalized health-risk information, preventive recommendations, and outdoor activity guidance based on assessed pollution conditions.

### Web Application

The Flask web application provides:

- Current AQI information
- Monitoring-station selection
- Next-day AQI forecasting
- Forecast explanations
- Pollutant and weather information
- Personalized health assessment
- Health alerts and recommendations

## Project Structure

```text
Chennai_AQI_Project/
│
├── chennai_aqi_flask/
│   ├── app.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── models/
│   ├── utils/
│   ├── templates/
│   └── static/
│
├── notebooks/
│   └── Chennai_AQI_Full_Pipeline-2.ipynb
│
├── data/
│   ├── chennai_aqi_weather_merged.csv
│   └── chennai_live_history.csv
│
├── results/
│   └── model_comparison.png
│
├── tests/
├── requirements-notebook.txt
├── README.md
└── .gitignore