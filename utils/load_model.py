import joblib
import os

MODEL_PATH = 'final_mobile_price_model.pkl'
SCALER_PATH = 'scaler.pkl'

def load_trained_model():
    """
    Load a pre-trained machine learning model from disk.

    This function attempts to load a serialized model object stored at the
    path specified by `MODEL_PATH`. If the file does not exist or loading fails,
    it raises an appropriate error.

    Returns
    -------
    model : object
        The deserialized machine learning model, typically a scikit-learn estimator.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist at `MODEL_PATH`.
    RuntimeError
        If there is an error during model loading (e.g., corrupted file, incompatible format).

    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")

def load_scaler():
    """
    Load a pre-trained data scaler from disk.

    This function attempts to load a serialized scaler object stored at the
    path specified by `SCALER_PATH`. If the file does not exist or loading fails,
    it raises an appropriate error.

    Returns
    -------
    scaler : object
        The deserialized scaler object, typically a scikit-learn scaler.

    Raises
    ------
    FileNotFoundError
        If the scaler file does not exist at `SCALER_PATH`.
    RuntimeError
        If there is an error during scaler loading (e.g., corrupted file, incompatible format).

    """
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")
    try:
        scaler = joblib.load(SCALER_PATH)
        return scaler
    except Exception as e:
        raise RuntimeError(f"Error loading scaler: {e}")
