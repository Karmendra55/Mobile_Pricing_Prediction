import random
import streamlit as st

def set_session_value(key, value):
    """
    Safely sets a value in Streamlit's session state.

    This function attempts to assign a given value to a specified key in 
    Streamlit's session state (`st.session_state`). If an error occurs, 
    it displays a warning message without interrupting execution.

    Parameters
    ----------
    key : str
        The name of the session state variable to set.
    value : any
        The value to assign to the session state variable.

    """
    try:
        st.session_state[key] = value
    except Exception as e:
        st.warning(f"Failed to set {key}: {e}")

def randomize_inputs():
    """
    Randomizes all input fields stored in Streamlit session state.

    This function generates random realistic values for predefined numerical,
    binary, and camera-related inputs, and stores them in `st.session_state`.

    Numerical inputs include battery power, clock speed, internal memory, RAM,
    number of CPU cores, phone weight, depth, talk time, screen resolution,
    and screen size.

    Binary inputs include features such as Bluetooth, dual SIM, 3G, 4G,
    WiFi, and touch screen support.

    Camera inputs include front and primary camera resolutions.

    Behavior
    --------
    - Generates randomized values for each input category.
    - Saves each generated value into `st.session_state` using `set_session_value`.

    Input Ranges
    ------------
    Numerical
    Binary:
        - "blue", "dual_sim", "three_g", "four_g", "wifi", "touch_screen":
          Randomly assigned 0 (No) or 1 (Yes).
    Camera:
        - fc: 0 to 20 MP
        - pc: 0 to 50 MP

    Notes
    -----
    - Requires Streamlit to be running with an active session state.
    - Random values can be used for testing or demonstration purposes.
    """
    
    # --- Numerical inputs ---
    numerical_inputs = {
        "battery_power": random.randint(500, 5000),
        "clock_speed": round(random.uniform(0.5, 3.0), 1),
        "int_memory": random.choice(range(2, 257, 4)),
        "ram": random.choice(range(128, 4097, 256)),
        "n_cores": random.randint(1, 12),
        "mobile_wt": random.randint(80, 250),
        "m_dep": round(random.uniform(0.1, 1.0), 2),
        "talk_time": random.randint(2, 24),
        "px_height": random.choice(range(100, 2001, 50)),
        "px_width": random.choice(range(100, 2001, 50)),
        "sc_h": random.randint(5, 20),
        "sc_w": random.randint(3, 10)
    }

    binary_inputs = ["blue", "dual_sim", "three_g", "four_g", "wifi", "touch_screen"]
    camera_inputs = {
        "fc": random.randint(0, 20),
        "pc": random.randint(0, 50) 
    }

    for key, value in {**numerical_inputs, **camera_inputs}.items():
        set_session_value(key, value)

    for key in binary_inputs:
        set_session_value(key, random.choice([0, 1]))