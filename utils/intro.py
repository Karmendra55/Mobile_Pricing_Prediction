import streamlit as st
from streamlit.components.v1 import html
import base64
import os

def add_intro_voice(audio_file_path: str):
    """
    Adds a styled play button in a Streamlit app to play an introductory audio clip.

    This function:
    - Adds custom CSS styling for the play button.
    - Checks whether the specified audio file exists.
    - Encodes the audio file to Base64 for inline playback.
    - Adds a button in the Streamlit app that plays the audio clip when clicked.

    Parameters
    ----------
    audio_file_path : str
        Path to the audio file (MP3 format recommended) to be played when the button is clicked.

    Behavior
    --------
    - Displays a custom-styled "Play" button using Streamlit's markdown and CSS injection.
    - If the file does not exist, shows an error message in the app.
    - Plays the audio inline without requiring external audio player controls.

    Exceptions
    ----------
    Displays an error message in the app if:
        - The audio file cannot be found at the given path.
        - The file cannot be read or encoded.
        
    """

    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #0dcaf0;
            color: #1e1e1e;
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 14px;
            font-weight: 500;
            border: none;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #0bb2d4;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- File Exists? ---
    if not os.path.exists(audio_file_path):
        st.error(f"Audio file not found: {audio_file_path}")
        return

    try:
        # --- Encode audio ---
        with open(audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        encoded_audio = base64.b64encode(audio_bytes).decode()
    except Exception as e:
        st.error(f"Failed to load audio: {e}")
        return

    # --- Play button ---
    if st.button("▶️ Play"):
        html(
            f"""
            <script>
                var audio = new Audio("data:audio/mp3;base64,{encoded_audio}");
                audio.play();
            </script>
            """,
            height=0,
        )
