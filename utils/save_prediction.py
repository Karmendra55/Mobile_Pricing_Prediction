import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Union, List
import numpy as np

def save_prediction_session(
    input_data: Dict[str, Union[int, float, None]],
    predicted_label: Union[int, np.integer],
    probabilities: Union[np.ndarray, List[float]],
    label_names: List[str]
) -> str:
    try:
        # Create timestamped folder
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = Path("Predictions") / timestamp
        folder_path.mkdir(parents=True, exist_ok=True)

        # --- Converts all input values to serializable Python types ---
        safe_input_data = {
            k: (
                0 if v is None or (isinstance(v, float) and np.isnan(v)) else
                float(v) if isinstance(v, (np.floating, float)) else
                int(v) if isinstance(v, (np.integer, int)) else
                v
            )
            for k, v in input_data.items()
        }

        # --- input.json ---
        input_path = folder_path / "input.json"
        with input_path.open("w") as f:
            json.dump(safe_input_data, f, indent=4)

        if isinstance(probabilities, np.ndarray):
            probabilities = probabilities.tolist()

        # --- prediction data ---
        prediction_data = {
            "predicted_label": int(predicted_label),
            "predicted_class": label_names[int(predicted_label)],
            "probabilities": probabilities
        }

        # --- Save prediction.json ---
        prediction_path = folder_path / "prediction.json"
        with prediction_path.open("w") as f:
            json.dump(prediction_data, f, indent=4)

        return str(folder_path)

    except Exception as e:
        print(f"❌ Failed to save prediction session: {e}")
        return ""
