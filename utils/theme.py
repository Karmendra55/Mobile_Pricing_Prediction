import streamlit as st
import os, json
import time

def apply_theme(theme):
    if theme == "Dark":
        css = """
        <style>
        html, body, .stApp {
            background-color: #0e1117 !important;
            color: #f5f5f5 !important;
            font-family: "Open Sans", sans-serif !important;
            transition: background-color 0.5s ease, color 0.5s ease;
        }

        .stSidebar, .stSidebarContent, header {
            background-color: #0e1117 !important;
            color: #f5f5f5 !important;
        }

        .stSlider label, .stSelectbox label, .stNumberInput label,
        .stRadio label, .stFileUploader label {
            color: #f5f5f5 !important;
        }
        
        .stTooltipIcon, .stSelectbox TooltipIcon {
            filter: invert(80%) sepia(20%) saturate(150%) hue-rotate(180deg);
        }

        .stTextInput input,
        .stNumberInput input,
        .stSelectbox div div div {
            background-color: #333 !important;
            color: #f5f5f5 !important;
        }

        /* Buttons (normal & download) */
        button {
            background-color: #2ecc71 !important;
            color: white !important;
            border: 1px solid #ffffff !important;
            border-radius: 8px !important;
            padding: 6px 16px !important;
            font-weight: bold !important;
            transition: background-color 0.3s ease, transform 0.3s;
        }

        button:hover {
            background-color: #27ae60 !important;
            color: #ffffff !important;
            transform: scale(0.98);
        }

        /* Ensure st.text() and st.markdown() text shows up white */
        .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
        .stText, .stText p, .stText span {
            color: #f5f5f5 !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        html, body, .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: "Segoe UI", sans-serif !important;
            transition: background-color 0.5s ease, color 0.5s ease;
        }

        .stSidebar, .stSidebarContent, header {
            background-color: #f8f9fa !important;
            color: #000000 !important;
        }

        .stSlider label, .stSelectbox label, .stNumberInput label,
        .stRadio label, .stFileUploader label {
            color: #000000 !important;
        }
        
        /* Buttons */
        button {
            background-color: #0d6efd !important;
            color: white !important;
            border-radius: 8px !important;
            border: 7px solid #0d6efd !important;
            transition: background-color 0.3s ease, transform 0.3s;
        }

        button:hover {
            transform: scale(0.98);
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# --- Cookies for theme ---
THEME_FILE = "theme_state.json"

def load_theme_from_file():
    try:
        if os.path.exists(THEME_FILE):
            with open(THEME_FILE, "r") as f:
                return json.load(f).get("theme", "Light")
    except Exception as e:
        print(f"Error loading theme: {e}")
    return "Light"

def save_theme_to_file(theme):
    with open(THEME_FILE, "w") as f:
        json.dump({"theme": theme}, f)

def init_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = load_theme_from_file()

# Theme toggle button ---
def theme_toggle_button():
    with st.sidebar:
        st.markdown("### 🎨 Theme")

        icon = "🌙" if st.session_state.theme == "Light" else "🌞"
        next_theme = "Dark" if st.session_state.theme == "Light" else "Light"

        clicked = st.button(f"{icon}")

        if clicked:
            st.markdown(
                """
                <style>
                #fade-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: white;
                    opacity: 0;
                    z-index: 9999;
                    animation: fadeout 0.6s forwards;
                }
                @keyframes fadeout {
                    0% { opacity: 0; }
                    50% { opacity: 0.7; }
                    100% { opacity: 0; display: none; }
                }
                </style>
                <div id="fade-overlay"></div>
                """,
                unsafe_allow_html=True
            )

            st.session_state.theme = next_theme
            save_theme_to_file(next_theme)
            time.sleep(0.6)
            st.rerun()

# --- Setup theme ---
def setup_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "Light"
    theme_toggle_button()
    apply_theme(st.session_state.theme)
