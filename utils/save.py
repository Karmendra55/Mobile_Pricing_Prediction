from fpdf import FPDF
from matplotlib import pyplot as plt
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from itertools import zip_longest

def create_download_path(folder_type: str, filename: str) -> str:
    base_path = Path("download") / folder_type
    base_path.mkdir(parents=True, exist_ok=True)
    return str(base_path / f"{filename}.pdf")


def save_probability_bar_image(probabilities_dict: Dict[str, float], title: str = "Probability Chart") -> BytesIO:
    fig, ax = plt.subplots(figsize=(6, 3))
    classes = list(probabilities_dict.keys())
    scores = list(probabilities_dict.values())

    ax.barh(classes, scores, color="skyblue")
    ax.set_xlabel("Probability")
    ax.set_title(title)
    plt.tight_layout()

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format="PNG")
    plt.close(fig)
    img_bytes.seek(0)
    return img_bytes


def generate_pdf_for_session(session_data: Dict[str, Any], folder_type: str = "single") -> str:
    try:
        session_id = session_data.get("timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
        pdf_path = create_download_path(folder_type, session_id)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # --- Titl e ---
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, f"Session Report: {session_id}", ln=True)

        # --- Prediction details ---
        prediction = session_data.get("prediction", {})
        pdf.set_font("Arial", size=12)
        for key, value in prediction.items():
            clean_value = str(value).replace("₹", "Rs.") if isinstance(value, (str, int, float)) else str(value)
            pdf.cell(0, 10, f"{key}: {clean_value}", ln=True)

        # --- probability bar chart ---
        class_probs = prediction.get("class_probabilities", {})
        if class_probs:
            pdf.ln(5)
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, "Class Probabilities:", ln=True)
            img = save_probability_bar_image(class_probs, title="Class Probabilities")
            pdf.image(img, x=10, w=180)

        pdf.output(pdf_path)
        return pdf_path

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return ""


def generate_combined_pdf(sessions: List[Dict[str, Any]], filename: str = "comparison_summary") -> str:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = create_download_path("multi", f"{filename}_{timestamp}")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for session in sessions:
            session_id = session.get("timestamp", "Unknown Session")
            prediction = session.get("prediction", {})
            probabilities = prediction.get("probabilities", [])

            pdf.add_page()
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, f"Session: {session_id}", ln=True)

            # --- Input features ---
            pdf.set_font("Arial", size=12)
            for k, v in session.get("input", {}).items():
                pdf.cell(0, 10, f"{k}: {v}", ln=True)

            # --- Prediction info ---
            pdf.ln(3)
            for k, v in prediction.items():
                if k != "probabilities":
                    clean_val = str(v).replace("₹", "Rs.") if isinstance(v, (str, int, float)) else v
                    pdf.cell(0, 10, f"{k}: {clean_val}", ln=True)

            labels = [
                "Low (<Rs.10k)", 
                "Medium (Rs.10k–30k)", 
                "High (Rs.30k–60k)", 
                "Very High (>Rs.60k)"
            ]
            class_probs = dict(zip_longest(labels, probabilities, fillvalue=0))
            img = save_probability_bar_image(class_probs, title="Prediction Probabilities")
            pdf.image(img, x=10, w=180)

        pdf.output(pdf_path)
        return pdf_path

    except Exception as e:
        print(f"❌ Combined PDF generation failed: {e}")
        return ""
