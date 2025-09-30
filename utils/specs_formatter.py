def format_spec_display(specs_dict):
    """
    Formats a dictionary of mobile specifications into a human-readable form.

    This function maps technical specification keys to descriptive labels and appends appropriate units.
    It also converts boolean-like numeric values (1/0) into "Yes"/"No" for better readability.

    Parameters
    ----------
    specs_dict : dict
        A dictionary containing mobile specification keys and their corresponding values.
        Example: {"sc_h": 15, "ram": 2048, "dual_sim": 1}

    Returns
    -------
    dict
        A dictionary with human-readable labels as keys and formatted values with units as values.
        Example: {"Screen Height": "15 cm", "RAM": "2048 MB", "Dual SIM Support": "Yes"}

    Behavior
    --------
    - If `specs_dict` is None or not a dictionary, returns an empty dictionary.
    - Uses a predefined mapping to convert keys to descriptive labels and attach units.
    - Converts boolean-like numeric values (1/0) to "Yes"/"No" for keys flagged as "YesNo".
    - Leaves unknown keys unchanged without units.

    """
    if not specs_dict or not isinstance(specs_dict, dict):
        return {}

    mapping = {
        "sc_h": ("Screen Height", "cm"),
        "int_memory": ("Internal Memory", "GB"),
        "touch_screen": ("Touch Screen", "YesNo"),
        "clock_speed": ("Processor Clock Speed", "GHz"),
        "fc": ("Front Camera", "MP"),
        "dual_sim": ("Dual SIM Support", "YesNo"),
        "px_width": ("Screen Width (px)", ""),
        "four_g": ("4G Support", "YesNo"),
        "px_height": ("Screen Height (px)", ""),
        "sc_w": ("Screen Width", "cm"),
        "wifi": ("WiFi Support", "YesNo"),
        "n_cores": ("CPU Cores", ""),
        "mobile_wt": ("Weight", "grams"),
        "three_g": ("3G Support", "YesNo"),
        "pc": ("Primary Camera", "MP"),
        "talk_time": ("Talk Time", "hrs"),
        "m_dep": ("Mobile Depth", "cm"),
        "blue": ("Bluetooth", "YesNo"),
        "ram": ("RAM", "MB"),
        "battery_power": ("Battery Power", "mAh")
    }

    formatted = {}
    for k, v in specs_dict.items():
        label, unit = mapping.get(k, (k, ""))
        if unit == "YesNo":
            formatted[label] = "Yes" if v == 1 else "No"
        else:
            formatted[label] = f"{v} {unit}".strip()
    return formatted
