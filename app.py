import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="Maintenance Copilot",
    layout="wide"
)

st.title("🔧 Maintenance Copilot")
st.write("Combines manuals, sensor metrics, and image evidence.")

manual = st.file_uploader(
    "📄 Upload Maintenance Manual (PDF)",
    type="pdf"
)

image = st.file_uploader(
    "📷 Upload Equipment Image",
    type=["jpg", "jpeg", "png"]
)

st.subheader("📡 Sensor Metrics")

temperature = st.slider(
    "Motor Temperature (°C)",
    0, 150, 70
)

vibration = st.slider(
    "Vibration (mm/s)",
    0.0, 15.0, 2.0
)

pressure = st.slider(
    "Pressure (PSI)",
    0, 100, 75
)

current = st.slider(
    "Current (A)",
    0, 50, 15
)

if st.button("Analyze"):

    manual_text = ""

    if manual:
        reader = PdfReader(manual)

        for page in reader.pages:
            text = page.extract_text()
            if text:
                manual_text += text + "\n"

    severity = "Normal"
    issue = "System Operating Normally"

    recommendation = """
Continue routine inspection.
Monitor sensor values.
Follow maintenance schedule.
"""

    manual_reference = """
Equipment operating within normal limits.
"""

    if temperature > 90:

        severity = "Critical"
        issue = "Motor Overheating"

        recommendation = """
• Check cooling fan
• Improve ventilation
• Clean dust deposits
• Reduce operating load
"""

        manual_reference = """
If motor temperature exceeds 90°C:
Check cooling fan and ventilation.
Stop operation above 100°C.
"""

    elif vibration > 6:

        severity = "Warning"
        issue = "Bearing Failure Risk"

        recommendation = """
• Inspect bearings
• Check lubrication
• Replace damaged bearings
"""

        manual_reference = """
High vibration indicates bearing wear.
Inspect bearings and lubrication.
"""

    elif pressure < 50:

        severity = "Critical"
        issue = "Hydraulic Leakage"

        recommendation = """
• Inspect pipe joints
• Check seals
• Tighten loose connections
"""

        manual_reference = """
Pressure below operating range may
indicate leakage in the system.
"""

    elif current > 25:

        severity = "Critical"
        issue = "Electrical Overload"

        recommendation = """
• Inspect motor winding
• Check power supply
• Verify load conditions
"""

        manual_reference = """
High current draw indicates overload.
Inspect motor and power supply.
"""

    st.subheader("📋 Maintenance Report")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Temperature", f"{temperature} °C")
        st.metric("Vibration", f"{vibration} mm/s")

    with col2:
        st.metric("Pressure", f"{pressure} PSI")
        st.metric("Current", f"{current} A")

    st.info(f"Detected Issue: {issue}")

    if severity == "Critical":
        st.error(f"Severity: {severity}")
    elif severity == "Warning":
        st.warning(f"Severity: {severity}")
    else:
        st.success(f"Severity: {severity}")

    st.markdown("### 🛠 Recommended Actions")
    st.write(recommendation)

    st.markdown("### 📖 Manual Reference")
    st.write(manual_reference)

    if manual_text:
        with st.expander("View Uploaded Manual"):
            st.write(manual_text[:2000])

    if image:

        img = Image.open(image)

        st.markdown("### 📷 Image Evidence")
        st.image(img, width=450)

    st.success("Analysis Completed Successfully")
