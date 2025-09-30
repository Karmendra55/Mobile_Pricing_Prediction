import numpy as np

def predict_price_range(model, scaler, input_data):
    """
    Predicts the price range category of a mobile phone based on its specifications.

    This function takes user input specifications, scales them, and uses a trained
    machine learning model to predict the price range and associated probabilities.

    Parameters
    ----------
    model : object
    scaler : object
    input_data : dict

    Returns
    -------
    price_label : str
    probabilities : list of float

    Raises
    ------
    ValueError
        If any required feature is missing in `input_data`.
    RuntimeError
        If prediction fails for other reasons (e.g., incompatible input shape).

    """
    feature_order = [
        'battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc',
        'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores',
        'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w',
        'talk_time', 'three_g', 'touch_screen', 'wifi'
    ]
    
    try:

        values = [input_data[feature] for feature in feature_order]
        scaled_values = scaler.transform([values])

        prediction = model.predict(scaled_values)[0]
        probabilities = model.predict_proba(scaled_values)[0]
        price_map = {
            0: "Low (<₹10k)",
            1: "Medium (₹10k-₹30k)",
            2: "High (₹30k-₹60k)",
            3: "Very High (>₹60k)"
        }
        price_label = price_map.get(prediction, "Unknown")

        return price_label, probabilities

    except KeyError as ke:
        raise ValueError(f"Missing input feature: {ke}")
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")
