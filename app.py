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

    issues = []
    recommendations = []
    references = []
    severity = "Normal"

    if temperature > 90:
        issues.append("🔥 Motor Overheating")
        recommendations.append(
            "Check cooling fan, improve ventilation, clean dust deposits."
        )
        references.append(
            "Manual: Temperature above 90°C indicates overheating."
        )
        severity = "Critical"

    if vibration > 6:
        issues.append("⚙️ Bearing Failure Risk")
        recommendations.append(
            "Inspect bearings and check lubrication."
        )
        references.append(
            "Manual: High vibration may indicate bearing wear."
        )
        if severity != "Critical":
            severity = "Warning"

    if pressure < 50:
        issues.append("💧 Hydraulic Leakage")
        recommendations.append(
            "Inspect pipe joints and replace damaged seals."
        )
        references.append(
            "Manual: Pressure below 50 PSI may indicate leakage."
        )
        severity = "Critical"

    if current > 25:
        issues.append("⚡ Electrical Overload")
        recommendations.append(
            "Inspect motor winding and power supply."
        )
        references.append(
            "Manual: Current above 25A indicates overload."
        )
        severity = "Critical"

    if not issues:
        issues.append("✅ System Operating Normally")
        recommendations.append(
            "Continue routine inspection and maintenance."
        )
        references.append(
            "Manual: All parameters within normal range."
        )

    st.subheader("📋 Maintenance Report")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Temperature", f"{temperature} °C")
        st.metric("Vibration", f"{vibration} mm/s")

    with col2:
        st.metric("Pressure", f"{pressure} PSI")
        st.metric("Current", f"{current} A")

    st.markdown("### 🚨 Detected Issues")

    for issue in issues:
        st.write(issue)

    if severity == "Critical":
        st.error(f"Severity: {severity}")
    elif severity == "Warning":
        st.warning(f"Severity: {severity}")
    else:
        st.success(f"Severity: {severity}")

    st.markdown("### 🛠 Recommended Actions")

    for rec in recommendations:
        st.write("•", rec)

    st.markdown("### 📖 Manual References")

    for ref in references:
        st.write("•", ref)

    if manual_text:
        with st.expander("View Uploaded Manual"):
            st.write(manual_text[:2000])

    if image:
        img = Image.open(image)

        st.markdown("### 📷 Image Evidence")
        st.image(img, width=450)

    st.success("Analysis Completed Successfully")
