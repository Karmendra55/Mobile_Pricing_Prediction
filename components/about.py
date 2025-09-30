import streamlit as st

def render_about_sidebar():
    """
    Renders the "About" section in the Streamlit sidebar with expandable information panels.

    This function adds an informational sidebar section to the app, containing
    details about the application's purpose, prediction methodology, model details,
    key features, and author credits. Each section is collapsible for improved readability.

    Sections Included
    -----------------
    1. What is this app?
    2. How does it predict?
    3. Model Details
    4. Outputs & Features
    5. Feedback & Credits

    Behavior
    --------
    - Uses expandable sections (`st.expander`) to display information neatly.
    - Displays section titles with relevant emojis for visual clarity.
    - Handles exceptions gracefully and displays an error message if rendering fails.

    """
    try:
        with st.sidebar:
            st.markdown("### ℹ️ About")

            def expander(title: str, content: str):
                with st.expander(title):
                    st.markdown(content)

            expander("📘 What is this app?", """
                The **Mobile Price Range Predictor** estimates the price range of a smartphone based on its specifications.
                It is useful for quick evaluations, resale pricing, and educational purposes.
            """)

            expander("🤖 How does it predict?", """
                The model uses hardware, camera, connectivity, and screen features to classify devices into:
                - 0: Low (< ₹10k)
                - 1: Medium (₹10k–₹30k)
                - 2: High (₹30k–₹60k)
                - 3: Very High (> ₹60k)
            """)

            expander("🧠 Model Details", """
                - **Algorithm**: Random Forest Classification  
                - **Accuracy**: ~89% on validation  
                - **Training Data**: 2,000+ cleaned samples  
                - **Preprocessing**: MinMax scaling + feature selection  
            """)

            expander("📄 Outputs & Features", """
                - Probabilistic predictions  
                - PDF report generation  
                - Session-based comparison across predictions  
                - Parody Comparison System  
                - Theme Changing Option  
            """)

            expander("📬 Feedback & Credits", """
                - Developed by **Karmendra Bahadur Srivastava**  
                - Thanks to **'Mark'** Voice powered by Elevenslab  
                - Email: **[Click Me](mailto:karmendra5902@gmail.com)**  
                - Dataset by Unified Mentor ML Repository  
            """)

    except Exception as e:
        st.error(f"An error occurred while loading the About section: {e}")
