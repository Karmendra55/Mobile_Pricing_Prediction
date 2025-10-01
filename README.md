# Mobile Phone Pricing Prediction

A Streamlit-based web application to predict mobile phone prices using specifications, compare predictions across multiple inputs, and view structured phone specification data in a clean format.

## Dataset Layout

The Dataset and Models are already in place, If you want to change the files you can replace these:

``` markdown
> Original_dataset/
>    dataset.csv
> ../
>    Clean_Mobile_Data.csv

> ../
>    final_mobile_price_model.pkl
>    best_rd_model.pkl
>    scaler.pkl
```

make sure that all the files are present in the root folder.

## Quickstart

1) Create and activate a virtual environment
```bash
python -m venv .venv
```
For Linux or Max:
```bash
source .venv/bin/activate
```
For Windows:
```bash
.venv\Scripts\activate
```

2) Now Run the file to install the dependencies
```bash
install_modules.bat
```

Run the Application
3a) Option A
```bash
run.bat
```

3b) Option B
- Open the command/bash and do the follow:
```bash
cd {"Drive:/file/.../Mobile_Phone_Pricing/"}
```
and type
```bash
streamlit run main.py
```

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
