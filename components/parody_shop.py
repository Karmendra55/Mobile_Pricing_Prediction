import streamlit as st
from utils.parody_data import get_parody_phones
from utils.specs_formatter import format_spec_display

def extract_numeric_price(price_str):
    """
    Extracts and returns the numeric value from a price string.

    This function removes currency symbols, commas, and whitespace 
    from a price string, then converts it to an integer.
    If conversion fails, it returns 0.

    Parameters
    ----------
    price_str : str
        A string containing a price, possibly including currency symbols (e.g., "Rs."),
        commas, or extra spaces.
        Example: "Rs. 1,23,456"

    Returns
    -------
    int
        The numeric value of the price. Returns 0 if extraction or conversion fails.

    """
    try:
        return int(price_str.replace("Rs.", "").replace(",", "").strip())
    except:
        return 0

def parody_shop_interface():
    """
    Displays an interactive parody phone shop interface in a Streamlit app.

    This function creates a user interface for browsing, filtering, and viewing
    parody phones. Users can search by name, sort results, paginate through
    available phones, and view detailed specifications.

    Behavior
    --------
    - Displays a search bar to type or select a parody phone.
    - Offers sorting options: Name (A-Z), Name (Z-A), Price (Low to High), Price (High to Low).
    - Implements pagination for browsing phone listings (3 phones per page).
    - Displays a preview of key phone features and allows viewing full details.
    - Allows selecting a phone for comparison with the user's phone.
    - Shows detailed technical specifications with images when requested.

    Uses
    ----
    - `get_parody_phones()`: Retrieves the list of available parody phones.
    - `extract_numeric_price()`: Converts price strings to numeric values for sorting.
    - `format_spec_display()`: Formats specification data for display.

    State Management
    ----------------
    - Uses `st.session_state` to store:
        - Current page number (`current_page`)
        - Which phone's details are shown (`show_details_for`)
        - Selected phone for comparison (`compare_with_parody`)

    """
    st.write("### 🔍 Search a parody phone")

    phones = get_parody_phones()
    if not phones:
        st.warning("⚠️ No phones found.")
        return
    
    phone_names = [phone["name"] for phone in phones]

    col1, col2, col3 = st.columns([5,2,1])
    with col1:
        selected_name = st.selectbox(
            "Type or select a parody phone",
            options=[""] + phone_names,
            format_func=lambda x: "Select a phone..." if x == "" else x
        )

    with col2:
        # --- Filters ---
        sort_choice = st.selectbox("↕️ Sort Phones", ["Name (A-Z)", "Name (Z-A)", "Price (Low to High)", "Price (High to Low)"])
        if not selected_name:
            filtered_phones = phones
        else:
            filtered_phones = [p for p in phones if p["name"] == selected_name]

        if sort_choice == "Name (A-Z)":
            filtered_phones.sort(key=lambda x: x["name"])
        elif sort_choice == "Name (Z-A)":
            filtered_phones.sort(key=lambda x: x["name"], reverse=True)
        elif sort_choice == "Price (Low to High)":
            filtered_phones.sort(key=lambda x: extract_numeric_price(x["price"]))
        elif sort_choice == "Price (High to Low)":
            filtered_phones.sort(key=lambda x: extract_numeric_price(x["price"]), reverse=True)
            
        if not filtered_phones:
            st.warning("⚠️ No phones match your selection.")
            return
    with col3:
        # --- Pagination ---
        PHONES_PER_PAGE = 3
        total_pages = (len(filtered_phones) - 1) // PHONES_PER_PAGE + 1

        if "current_page" not in st.session_state:
            st.session_state.current_page = 1

        def on_page_change():
            st.session_state.page_changed = True

        current_page = st.selectbox(
            "📄 Page",
            options=list(range(1, total_pages + 1)),
            index=st.session_state.current_page - 1,
            format_func=lambda x: f"{x} of {total_pages}",
            key="current_page",
            on_change=on_page_change
        )

        if "page_changed" not in st.session_state:
            st.session_state.page_changed = False

        if st.session_state.page_changed:
            current_page = st.session_state.current_page
            st.session_state.page_changed = False
        else:
            current_page = st.session_state.current_page

        start_idx = (current_page - 1) * PHONES_PER_PAGE
        end_idx = start_idx + PHONES_PER_PAGE
        current_phones = filtered_phones[start_idx:end_idx]

    if "show_details_for" not in st.session_state:
        st.session_state["show_details_for"] = None

    if st.session_state["show_details_for"]:
        phone = next(p for p in phones if p["name"] == st.session_state["show_details_for"])
        specs = format_spec_display(phone["specs"])

        with st.container():
            st.markdown("## 📱 Detailed Phone View")
            col4, col5 = st.columns([1, 2])
            with col4:
                st.image(phone["image"], use_container_width=True)
            with col5:
                st.subheader(phone["name"])
                st.caption(phone["price"])
                st.markdown("### 🔧 Technical Specifications")
                if specs:
                    for label, value in specs.items():
                        st.markdown(f"- **{label}:** {value}")
                else:
                    st.info("No specifications available.")
                if st.button("🔙 Close Details"):
                    st.session_state["show_details_for"] = None
        return 

    for phone in current_phones:
        col6, col7 = st.columns([1, 3])
        with col6:
            st.image(phone["image"], width=120)
        with col7:
            st.subheader(phone["name"])
            st.caption(phone["price"])

            # --- Preview features ---
            preview_features = phone["features"][:3]
            st.markdown("**Key Features:**")
            for feat in preview_features:
                st.markdown(f"- {feat}")

            if st.button(f"📋 View Full Details", key="view_" + phone["name"]):
                st.session_state["show_details_for"] = phone["name"]
                st.rerun()

            if st.button(f"📊 Compare with My Phone", key="compare_" + phone["name"]):
                st.session_state["compare_with_parody"] = phone
                st.success(f"{phone['name']} selected for comparison.")

        st.markdown("---")

    if total_pages > 1:
        st.caption(f"Page {current_page} of {total_pages}")
