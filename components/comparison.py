import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import shutil

from utils.save import generate_pdf_for_session, generate_combined_pdf
from utils.specs_formatter import format_spec_display

PREDICTION_FOLDER = "Predictions"

def load_prediction_sessions():
    """Load all valid prediction sessions from disk."""
    if not os.path.exists(PREDICTION_FOLDER):
        return []

    sessions = []
    for folder in sorted(os.listdir(PREDICTION_FOLDER), reverse=True):
        try:
            folder_path = os.path.join(PREDICTION_FOLDER, folder)
            input_file = os.path.join(folder_path, "input.json")
            prediction_file = os.path.join(folder_path, "prediction.json")

            if os.path.exists(input_file) and os.path.exists(prediction_file):
                with open(input_file, "r", encoding="utf-8") as f:
                    input_data = json.load(f)
                with open(prediction_file, "r", encoding="utf-8") as f:
                    prediction_data = json.load(f)

                sessions.append({
                    "timestamp": folder,
                    "input": input_data,
                    "prediction": prediction_data
                })
        except Exception as e:
            st.warning(f"⚠️ Error loading session '{folder}': {e}")
    return sessions

def delete_selected_sessions(selected_ids):
    deleted = 0
    for session_id in selected_ids:
        try:
            folder_path = os.path.join(PREDICTION_FOLDER, session_id)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                deleted += 1
        except Exception as e:
            st.error(f"Failed to delete '{session_id}': {e}")
    return deleted

def display_comparison_table(sessions):
    if not sessions:
        st.info("📂 No prediction sessions found.")
        return

    data_rows = []
    for session in sessions:
        row = {"Timestamp": session["timestamp"]}
        row.update(session["input"])
        row["Predicted Class"] = session["prediction"].get("predicted_class", "N/A")
        data_rows.append(row)

    df = pd.DataFrame(data_rows)
    st.dataframe(df, use_container_width=True)


def plot_probability_bar(session):
    probs = session["prediction"].get("probabilities", [])
    labels = ["Low (<₹10k)", "Medium (₹10k–₹30k)", "High (₹30k–₹60k)", "Very High (>₹60k)"]

    if not probs or not isinstance(probs, list) or len(probs) != len(labels):
        st.warning("⚠️ Probability data missing or malformed.")
        return

    fig, ax = plt.subplots()
    ax.barh(labels, probs, color='red')
    ax.set_xlabel("Probability")
    ax.set_title(f"Prediction Probabilities — {session['timestamp']}")
    st.pyplot(fig)


def load_all_sessions_df():
    sessions = load_prediction_sessions()
    flat_data = []

    for session in sessions:
        try:
            row = session["input"].copy()
            row.update(session["prediction"])
            row["Session"] = session["timestamp"]
            flat_data.append(row)
        except Exception as e:
            st.warning(f"⚠️ Error processing session {session['timestamp']}: {e}")

    return pd.DataFrame(flat_data)

def flatten_sessions(sessions):
    flat_data = []
    for session in sessions:
        try:
            row = session["input"].copy()
            row.update(session["prediction"])
            row["session"] = session["timestamp"]
            flat_data.append(row)
        except Exception as e:
            st.warning(f"⚠️ Error processing session {session['timestamp']}: {e}")
    return pd.DataFrame(flat_data)

def comparison_app():
    sessions = load_prediction_sessions()

    if not sessions:
        st.info("No prediction sessions found.")
        return

    st.markdown("### 🔍 View Prediction Probability Breakdown")

    session_ids = [s["timestamp"] for s in sessions]
    select_all = st.checkbox("✅ Select All Sessions", value=False)

    if select_all:
        selected_sessions = session_ids
    else:
        selected_sessions = st.multiselect("📂 Select session(s) to visualize:", options=session_ids)

    col1, col2, col3, col4 = st.columns([5,5,8,9])

    with col1:
        if st.button("💾 Individual PDFs"):
            export_count = 0
            for sid in selected_sessions:
                session = next((s for s in sessions if s["timestamp"] == sid), None)
                if session:
                    generate_pdf_for_session(session, folder_type="multi")
                    export_count += 1
            st.success(f"✅ {export_count} PDF(s) saved to `/download/multi/`") if export_count else st.warning("No sessions were exported.")

    with col2:
        if st.button("💾 Combined PDF"):
            selected_data = [s for s in sessions if s["timestamp"] in selected_sessions]
            path = generate_combined_pdf(selected_data, filename="comparison_report")
            st.success(f"📁 Combined PDF saved to `{path}`")

    with col4:
        with st.expander("🗑️ Delete Sessions", expanded=False):
            if selected_sessions:
                confirm = st.checkbox("⚠️ Confirm delete selected sessions")
                if st.button("🚨 Delete Permanently", type="primary") and confirm:
                    deleted = delete_selected_sessions(selected_sessions)
                    st.success(f"🗑️ {deleted} session(s) deleted.")
                    st.rerun()
            else:
                st.info("Select sessions to delete.")
                
    st.divider()

    if len(selected_sessions) >= 2:
        for sid in selected_sessions:
            session = next((s for s in sessions if s["timestamp"] == sid), None)
            if session:
                with st.expander(f"📊 {sid} — {session['prediction'].get('predicted_class', 'Unknown')}"):
                    plot_probability_bar(session)

        df_sessions = flatten_sessions([s for s in sessions if s["timestamp"] in selected_sessions])

        if not df_sessions.empty:
            st.markdown("## 📈 Multi-Session Comparison Summary")
            st.dataframe(df_sessions)

            if "ram" in df_sessions.columns:
                st.markdown("#### 📊 RAM Used Per Session")
                st.bar_chart(df_sessions.set_index("session")["ram"])

            if "predicted_class" in df_sessions.columns:
                st.markdown("#### 📊 Predicted Class Distribution")
                st.bar_chart(df_sessions["predicted_class"].value_counts())

            if "ram" in df_sessions.columns and "battery_power" in df_sessions.columns:
                st.markdown("#### 🔬 RAM vs Battery vs Predicted Class")
                st.altair_chart(
                    alt.Chart(df_sessions).mark_circle(size=60).encode(
                        x="ram",
                        y="battery_power",
                        color="predicted_class",
                        tooltip=["session", "predicted_class", "ram", "battery_power"]
                    ).interactive(),
                    use_container_width=True
                )
        else:
            st.info("No data available for comparison.")
    else:
        st.info("Select **two or more** sessions to view comparison graphs.")

def parody_comparison():
    
    st.markdown("---")
    st.subheader("📱 Compare With Predefined Phone")

    parody = st.session_state.get("compare_with_parody")
    if not parody:
        st.warning("⚠️ No phone selected for comparison.")
        st.info("Go to the **📦 Shop Phones** tab to select a model.")
        return
    try:
        sessions = load_prediction_sessions()
    except Exception as e:
        st.error(f"❌ Failed to load prediction sessions: {e}")
        return

    if not sessions:
        st.warning("⚠️ No saved prediction sessions found.")
        return

    sessions.sort(key=lambda s: s.get("timestamp", ""), reverse=True)

    parody_name = parody.get("name", "Unknown Model")
    parody_price = parody.get("price", "N/A")
    parody_features = parody.get("features", [])
    parody_specs = parody.get("specs", {})

    features_md = "\n".join([f"- {feature}" for feature in parody_features]) if parody_features else "_N/A_"

    st.markdown(f"""
    **Comparing with:** `{parody_name}`  
    💰 **Price**: `{parody_price}`  
    🔧 **Features**:
    {features_md}
    """)

    if "selected_session_id" not in st.session_state:
        st.session_state.selected_session_id = sessions[0]["timestamp"]
    try:
        session_timestamps = [s["timestamp"] for s in sessions]
        selected_session_id = st.selectbox(
            "📂 Select a prediction session to compare:",
            options=session_timestamps,
            index=session_timestamps.index(st.session_state.selected_session_id),
            key="parody_session_selector"
        )
    except Exception as e:
        st.error(f"❌ Failed to list sessions: {e}")
        return

    selected_session = next((s for s in sessions if s["timestamp"] == selected_session_id), None)
    if not selected_session:
        st.warning("⚠️ Could not find the selected session.")
        return

    user_specs = selected_session.get("input", {})
    user_prediction = selected_session.get("prediction", {}).get("predicted_class", "N/A")

    formatted_user = format_spec_display(user_specs or {})
    formatted_parody = format_spec_display(parody_specs or {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 Your Prediction")
        st.markdown(f"**Session**: `{selected_session_id}`")
        st.markdown(f"📊 **Predicted Class**: `{user_prediction}`")
        with st.expander("📱 View Your Specs"):
            if formatted_user:
                for key, val in formatted_user.items():
                    st.write(f"**{key}:** {val}")
            else:
                st.info("No user specifications found.")

    with col2:
        st.markdown("### 🎭 Selected Phone")
        st.markdown(f"**Model**: `{parody_name}`")
        st.markdown(f"💰 **Price**: `{parody_price}`")
        with st.expander("🤖 View Parody Specs"):
            if formatted_user:
                for key in formatted_user:
                    parody_value = formatted_parody.get(key, "N/A")
                    st.write(f"**{key}:** {parody_value}")
            else:
                st.info("No parody specs found.")

    if st.button("❌ Clear Specification Comparison"):
        st.session_state.pop("compare_with_parody", None)
        st.session_state.pop("selected_session_id", None)
        st.rerun()