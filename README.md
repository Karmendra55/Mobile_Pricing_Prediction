# Phone Price Prediction and Comparison Web App

This Streamlit web application allows users to:
- Predict the price of a mobile phone using specifications.
- Compare predicted prices across multiple inputs.
- View cleaned and formatted phone specifications.

---

## ‍Developed By
- **Karmendra Bahadur Srivastava**
- **Submitted To:** Unified Mentor  

---

## Features

- Predict phone prices based on features like RAM, Battery, Camera, etc.
- Save and manage multiple prediction sessions.
- Compare predictions side-by-side.
- View mobile specifications in a user-friendly format.

---

Model Information

Model trained on phone specifications dataset (e.g., Mobile Price Classification).
Uses features like RAM, battery power, clock speed, etc.
You can modify or replace model.pkl inside the prediction/ directory with your own.

---

Technologies Used

Python
Streamlit
scikit-learn
pandas
joblib

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phone-price-predictor.git
   cd phone-price-predictor

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

## Run the Program
>> streamlit run main.py
Or
Open the run.bat file in the root folder.

---