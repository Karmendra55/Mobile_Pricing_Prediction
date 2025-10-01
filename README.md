# Mobile Phone Pricing Prediction

A Streamlit-based web application to predict mobile phone prices using specifications, compare predictions across multiple inputs, and view structured phone specification data in a clean format.

## Dataset Layout

The Dataset and Models are already in place, If you want to change the files you can replace these:

``` markdown
> Original_dataset/
>    dataset.csv

> trained_model/
>    thyroid_recurrence_rf.pkl
>    thyroid_recurrence_rf_only.pkl
```

make sure that all the files are present in the root folder.

## Quickstart



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

- Model: Random Forest Classification model trained using scikit-learn.
- Dataset: Mobile price/specification dataset with features like:
   - RAM, Internal Memory, Battery, Clock Speed
   - Number of Cores, Front/Back Camera, Weight, etc.
- Output: Predicted price range or exact price depending on model type.

## Highlights

- Interactive and clean UI using Streamlit.
- Modular design with separation of logic, UI, and helpers.
- Saves sessions to view and compare past predictions.
- Supports running via .bat for quick local execution.

## Features

1. Phone Price Predictor → Accepts inputs like RAM, camera, battery, clock speed, etc., and predicts the price using a trained ML model.
2. Session Manager → Each prediction is stored with a timestamp and can be viewed or deleted later.
3. Comparison Tool → Allows side-by-side price comparison of multiple phone configurations.
4. Parody Shop → Simulated product listing interface for user-customized phones.
5. Specification Formatter → Converts raw data into a clean, human-readable spec sheet.
