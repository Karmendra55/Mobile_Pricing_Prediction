import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_prediction_probabilities(probabilities):
    """
    Plots a horizontal bar chart showing the model's predicted probabilities for each price range category.

    Parameters
    ----------
    probabilities : iterable of float
        A list or array-like structure containing probability values for each price range category.
        Expected length is 4, corresponding to: Low, Medium, High, Very High
        Probabilities should be in the range [0, 1].

    Behavior
    --------
    - Converts the probabilities into a pandas DataFrame with corresponding labels.
    - Creates a horizontal bar chart using Matplotlib.
    - Displays probabilities as percentages next to each bar.
    - Handles errors gracefully and displays an error message in Streamlit if plotting fails.

    """
    labels = ["Low (<₹10k)", "Medium (₹10k–₹30k)", "High (₹30k–₹60k)", "Very High (>₹60k)"]
    try:
        prob_df = pd.DataFrame({'Price Range': labels, 'Probability': list(map(float, probabilities))})
    except Exception as e:
        st.error(f"❌ Error processing probabilities: {e}")
        return

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(8, 3))
    bars = ax.barh(prob_df['Price Range'], prob_df['Probability'], color='#0d6efd')
    ax.set_xlim(0, 1)
    ax.set_xlabel('Probability')
    ax.set_title('📊 Model Confidence per Class')

    for i, (prob, label) in enumerate(zip(prob_df['Probability'], prob_df['Price Range'])):
        ax.text(prob + 0.01, i, f'{prob:.2%}', va='center', color='black', fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)
