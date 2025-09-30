import streamlit as st
import os

from utils.load_model import load_trained_model, load_scaler
from utils.predictor import predict_price_range
from utils.theme import apply_theme, theme_toggle_button, load_theme_from_file
from utils.random import randomize_inputs
from utils.save_prediction import save_prediction_session
from utils.intro import add_intro_voice

from components.vis import plot_prediction_probabilities
from components.comparison import comparison_app, parody_comparison
from components.about import render_about_sidebar
from components.parody_shop import parody_shop_interface

st.set_page_config(page_title="Mobile Price Predictor", layout="centered")

def ensure_download_dirs():
    os.makedirs("download/single", exist_ok=True)
    os.makedirs("download/multi", exist_ok=True)
try:
    ensure_download_dirs()
except FileNotFoundError():
    st.error("The Folders and Files are missing, Kindly download all the files.")

# --- Theme ---
if "theme" not in st.session_state:
    st.session_state.theme = load_theme_from_file()
apply_theme(st.session_state.theme)
theme_toggle_button()

render_about_sidebar()

# --- Voice ---
with st.sidebar:    
    st.subheader("❓ How does this work?")
    add_intro_voice("intro/Voice.mp3")

try:
    model = load_trained_model()
    scaler = load_scaler()
except Exception as e:
    st.error("🚨 Failed to load model or scaler. Please check the files.")
    st.stop()

# --- Title ---
st.title("📱 Mobile Price Predicition System")

# --- Price Mapping ---
class_mapping = {
    0: "Low (<₹10k)",
    1: "Medium (₹10k-₹30k)",
    2: "High (₹30k-₹60k)",
    3: "Very High (>₹60k)"
}
class_names = list(class_mapping.values())

tab1, tab2, tab3= st.tabs(["📱 Predict Price Range", "📊 Compare Past Predictions", "🛒 Some Popular Phones"])

# --- Prediction Tab ---
with tab1:
    st.subheader("Mobile Price Range Prediction")
    st.markdown("Enter your mobile phone specifications below to predict its price range.")
    if st.button("🎲 Randomize All Inputs"):
        randomize_inputs()
        
    with st.form("input_form"):
        st.subheader("🔧 Performance Specification")
        st.slider("RAM (MB)", 128, 4096, step=128, value=1024, key="ram",
                    help="Memory available for running tasks. More Random Access Memory(RAM) can improve multitasking.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.slider("Internal Memory (GB)", 2, 256, step=2, value=64, key="int_memory",
                    help="Built-in storage capacity to store for application and media.")
        with col2:
            st.slider("Clock Speed (GHz)", 0.5, 3.0, step=0.1, value=1.5, key="clock_speed",
                    help="Processing speed of the CPU Processor. Faster speeds improve performance.")
        with col3:
            st.slider("Processor Cores", 1, 12, step=1, value=4, key="n_cores",
                    help="Number of CPU cores. More cores may help with performance and multi-tasking.")
        
        st.subheader("🔋 Power Usage")
        col4, col5 = st.columns([2,1])
        with col4:
            st.slider("Battery Power (mAh)", 500, 5000, step=50, value=2500, key="battery_power",
                    help="Total battery capacity. Higher capacity will allow user for longer usage.")
        with col5:
            st.slider("Talk Time (hours)", 2, 24, step=1, value=10, key="talk_time",
                    help="Maximum talk time after a full charge.")  
        
        st.subheader("📡 Connectivity Features")
        col6, col7, col8, col9, col10, col11 = st.columns(6)
        with col6:
            st.selectbox("Bluetooth", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", key="blue",
                     help="Whether the device supports Bluetooth connectivity.")
        with col9:
            st.selectbox("4G Support", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", key="four_g",
                     help="Is 4G Internet supported?")
        with col7:
            st.selectbox("Dual SIM", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", key="dual_sim",
                     help="Is the phone supporting one or two SIM cards simultaneously")
        with col10:
            st.selectbox("WiFi Support", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", key="wifi",
                     help="Whether the device supports WiFi connectivity.")
        with col8:
            st.selectbox("3G Support", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", key="three_g",
                     help="Is 3G Internet Supported?")
        with col11:
            st.selectbox("Touch Screen", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No", key="touch_screen",
                     help="Is the device touch screen?")

        st.subheader("📸 Camera Quality")
        col12, col13 = st.columns(2)
        with col12:
            st.slider("Front Camera (MP)", 0, 20, step=1, value=5, key="fc",
                      help="Front camera megapixel rating.")
        with col13:
            st.slider("Primary/Rear Camera (MP)", 0, 50, step=1, value=12, key="pc",
                      help="Primary rear camera megapixel rating.")

        st.subheader("📱 Screen Display Visuals")
        col14, col15= st.columns(2)
        with col14:
            st.slider("Display Height (Px)", 100, 2000, step=50, value=1000, key="px_height",
                      help="Height of the display in pixels.") 
        with col15:
            st.slider("Display Width (Px)", 100, 2000, step=50, value=1000, key="px_width",
                      help="Width of the display in pixels.")
            
        st.subheader("🖥️ Hardware Screen Specifications")    
        col16, col17= st.columns(2) 
        with col16:
            st.slider("Screen Height (cm)", 5, 20, step=1, value=10, key="sc_h",
                      help="The Physical screen height.")
        with col17:
            st.slider("Screen Width (cm)", 3, 10, step=1, value=5, key="sc_w",
                      help="The Physical screen width.")
        col18, col19 = st.columns([1,2])
        with col18:
            st.slider("Mobile Depth (cm)", 0.1, 1.0, step=0.01, value=0.5, key="m_dep",
                    help="Thickness of the Device.")
        with col19:
            st.slider("Weight (grams)", 80, 250, step=5, value=150, key="mobile_wt",
                        help="Total weight of the device in grams.")
        
        # --- Predict button ---
        submit = st.form_submit_button("🔮 Predict Price Range")

        # --- After submission ---
        if submit:
            with st.spinner("Predicting..."):
                input_data = {k: v for k, v in st.session_state.items() if k in [
                    'battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g',
                    'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height',
                    'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g',
                    'touch_screen', 'wifi'
                ]}
                price_label, probabilities = predict_price_range(model, scaler, input_data)
                
                st.session_state["last_input"] = input_data
                st.session_state["last_prediction"] = price_label
                st.session_state["show_result"] = True
                
                # --- S ave prediction ---
                save_prediction_session(
                    input_data=input_data,
                    predicted_label=class_names.index(price_label),
                    probabilities=probabilities,
                    label_names=class_names
                )

                # --- Display result ---
                st.markdown(f"""
                    <div style='padding: 1rem; background-color: #D1E7DD; border-radius: 10px; 
                                border: 2px solid #0F5132; text-align: center;'>
                        <h2 style='color: #0F5132;'>Predicted Price Range</h2>
                        <h1 style='color: #0F5132;'>{price_label}</h1>
                    </div>
                """, unsafe_allow_html=True)

                plot_prediction_probabilities(probabilities)
                st.info("📍 View detailed comparisons in the 'Compare Past Predictions' tab.")
            
# --- Comparison Tab ---
with tab2:
    st.header("📊 Compare Past Predictions")
    comparison_app()
    
# --- Popular Phones ---
with tab3:
    st.header("🛒 Popular Phones")

    subtab1, subtab2 = st.tabs(["📦 Shop Phones", "📊 Compare with Your Prediction"])

    with subtab1:
        parody_shop_interface()

    with subtab2:
        parody_comparison()
    