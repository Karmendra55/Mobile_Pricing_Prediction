# Mobile Phone Pricing Prediction

This Streamlit web application allows users to:
- Predict the price of a mobile phone using specifications.
- Compare predicted prices across multiple inputs.
- View cleaned and formatted phone specifications.

## Features

- Predict phone prices based on features like RAM, Battery, Camera, etc.
- Save and manage multiple prediction sessions.
- Compare predictions side-by-side.
- View mobile specifications in a user-friendly format.

## Installation

> Run the `install_modules.bat` file 
then follow the steps below

python -m venv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

Make sure all the files are present in the root folder

pip install -r requirements.txt

## Run the Program
>> streamlit run main.py
Or
> Open the `run.bat` file in the root folder.

## Model

>Model: Random Forest Classification model trained using scikit-learn.
>Dataset: Mobile price/specification dataset with features like:
   a)RAM, Internal Memory, Battery, Clock Speed
   b)Number of Cores, Front/Back Camera, Weight, etc.
>Output: Predicted price range or exact price depending on model type.

## Highlights

- Interactive and clean UI using Streamlit.
- Modular design with separation of logic, UI, and helpers.
- Saves sessions to view and compare past predictions.
- Supports running via .bat for quick local execution.

## Features

Phone Price Predictor → Accepts inputs like RAM, camera, battery, clock speed, etc., and predicts the price using a trained ML model.
Session Manager → Each prediction is stored with a timestamp and can be viewed or deleted later.
Comparison Tool → Allows side-by-side price comparison of multiple phone configurations.
Parody Shop → Simulated product listing interface for user-customized phones.
Specification Formatter → Converts raw data into a clean, human-readable spec sheet.
