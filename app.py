import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Maintenance Copilot",
    layout="wide"
)

st.title("🔧 Maintenance Copilot")
st.write("Monitor equipment health using sensor data and image evidence.")

image = st.file_uploader(
    "Upload Equipment Image",
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

    severity = "Normal"
    issue = "System Operating Normally"

    recommendation = """
✅ Equipment operating within safe limits.

• Continue routine inspection
• Monitor sensor values
• Follow maintenance schedule
"""

    if temperature > 90:

        severity = "Critical"

        issue = "Motor Overheating"

        recommendation = """
• Check cooling fan
• Improve ventilation
• Clean dust deposits
• Stop operation if temperature exceeds 100°C
"""

    elif vibration > 6:

        severity = "Warning"

        issue = "Bearing Failure Risk"

        recommendation = """
• Inspect bearings
• Check lubrication
• Replace damaged bearings
"""

    elif pressure < 50:

        severity = "Critical"

        issue = "Hydraulic Leakage"

        recommendation = """
• Inspect pipe joints
• Check seals
• Tighten loose connections
"""

    elif current > 25:

        severity = "Critical"

        issue = "Electrical Overload"

        recommendation = """
• Inspect motor winding
• Check power supply
• Verify load conditions
"""

    st.subheader("📋 Maintenance Report")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Temperature",
            f"{temperature} °C"
        )

        st.metric(
            "Vibration",
            f"{vibration} mm/s"
        )

    with col2:
        st.metric(
            "Pressure",
            f"{pressure} PSI"
        )

        st.metric(
            "Current",
            f"{current} A"
        )

    st.info(f"**Detected Issue:** {issue}")

    if severity == "Critical":
        st.error(f"Severity: {severity}")

    elif severity == "Warning":
        st.warning(f"Severity: {severity}")

    else:
        st.success(f"Severity: {severity}")

    st.markdown("### 🛠 Recommended Actions")
    st.write(recommendation)

    if image:

        img = Image.open(image)

        st.markdown("### 📷 Image Evidence")
        st.image(img, width=450)

    st.success("Analysis Completed")
