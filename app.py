import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image

st.set_page_config(
    page_title="Maintenance Copilot",
    layout="wide"
)

st.title("🔧 Maintenance Copilot")
st.write("Combine maintenance manuals, sensor events, and image evidence.")

manual = st.file_uploader(
    "Upload Maintenance Manual (PDF)",
    type="pdf"
)

sensor_event = st.text_area(
    "Enter Sensor Event",
    height=200,
    placeholder="""
Asset ID: MTR-101
Event Time: 2026-06-11 10:30 AM

Sensor Readings:
Motor Temperature: 95°C
Normal Range: 60°C - 85°C

Alert Level: Critical

Observation:
Motor housing feels unusually hot.
"""
)

image = st.file_uploader(
    "Upload Equipment Image",
    type=["jpg", "jpeg", "png"]
)

if st.button("Analyze"):

    if not manual:
        st.error("Please upload a maintenance manual PDF.")
        st.stop()

    manual_text = ""

    reader = PdfReader(manual)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            manual_text += text + "\n"

    sensor = sensor_event.lower()

    severity = "Medium"
    issue = "Manual Inspection Required"
    recommendation = "No matching maintenance rule found."
    manual_section = "General Maintenance"

    if "temperature" in sensor or "hot" in sensor:

        severity = "Critical"
        issue = "Motor Overheating"

        recommendation = """
• Check cooling fan
• Inspect ventilation path
• Clean dust deposits
• Stop operation if temperature exceeds safety limits
"""

        manual_section = "Overheating"

    elif "vibration" in sensor or "noise" in sensor:

        severity = "Warning"
        issue = "Bearing Failure Risk"

        recommendation = """
• Inspect bearings
• Check lubrication
• Replace damaged bearings
"""

        manual_section = "Bearing Failure"

    elif "pressure" in sensor or "leakage" in sensor:

        severity = "Critical"
        issue = "Hydraulic Leakage"

        recommendation = """
• Inspect pipe joints
• Check seals
• Tighten loose connections
"""

        manual_section = "Leakage"

    elif "current" in sensor or "breaker" in sensor:

        severity = "Critical"
        issue = "Electrical Overload"

        recommendation = """
• Inspect motor winding
• Check power supply
• Verify load conditions
"""

        manual_section = "Electrical Fault"

    st.subheader("📋 Maintenance Report")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**Detected Issue:** {issue}")
        st.warning(f"**Severity:** {severity}")

    with col2:
        st.success(f"**Manual Section:** {manual_section}")

    st.markdown("### 📡 Sensor Event")
    st.code(sensor_event)

    st.markdown("### 🛠 Recommended Actions")
    st.write(recommendation)

    st.markdown("### 📖 Manual Reference")

    if manual_text:
        st.write(manual_text[:1500])

    if image:

        img = Image.open(image)

        st.markdown("### 📷 Image Evidence")
        st.image(img, width=400)

    st.success("Analysis Completed Successfully")
