# Air Quality Prediction Pipeline

This project provides a pipeline for air quality prediction using historical data, lagged features, and machine learning. The pipeline integrates with **Hopsworks Feature Store** and includes four main parts:

## 1. Feature Backfill
- Collects and backfills historical air quality data.
- Configures sensor metadata (location, type).
- Uploads processed data to the **Hopsworks Feature Store**.

## 2. Daily Feature Pipeline
- Downloads new daily air quality and weather data.
- Generates lagged features to capture temporal patterns.
- Automates daily updates with orchestration tools.

## 3. Training Pipeline
- Selects features and creates training datasets.
- Trains machine learning models with lagged features.
- Registers trained models in the **Hopsworks Model Registry**.

## 4. Batch Inference
- Loads trained models and performs batch predictions.
- Forecasts air quality and uploads results to the feature store.

## Lagged Features
Lagged features (e.g., past PM2.5, temperature) are engineered to improve model performance by capturing historical trends.

## Setup
1. Create a [Hopsworks.ai](https://www.hopsworks.ai/) account and obtain an API key.
2. Install dependencies (`hopsworks`, `pandas`, `scikit-learn`).
3. Execute the notebooks in sequence to backfill data, update features daily, train models, and perform inference.
