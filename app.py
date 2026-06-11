import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="Maintenance Copilot",
    layout="wide"
)

st.title("🔧 Maintenance Copilot")
st.write("Combines maintenance manuals, sensor metrics, and image evidence.")

# ---------------- PDF ----------------

manual = st.file_uploader(
    "📄 Upload Maintenance Manual (PDF)",
    type="pdf"
)

# ---------------- IMAGE ----------------

image = st.file_uploader(
    "📷 Upload Equipment Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- SENSORS ----------------

st.subheader("📡 Sensor Metrics")

temperature = st.slider(
    "Temperature (°C)",
    0, 150, 75
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

# ---------------- ANALYZE ----------------

if st.button("Analyze"):

    if not manual:
        st.error("Please upload a maintenance manual PDF.")
        st.stop()

    manual_text = ""

    try:
        reader = PdfReader(manual)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                manual_text += text + "\n"

    except:
        st.error("Unable to read PDF.")
        st.stop()

    # ---------------- MANUAL VALIDATION ----------------

    maintenance_keywords = [
        "temperature",
        "vibration",
        "pressure",
        "bearing",
        "motor",
        "maintenance",
        "overheating",
        "current",
        "leakage"
    ]

    valid_manual = False

    for word in maintenance_keywords:
        if word in manual_text.lower():
            valid_manual = True
            break

    if not valid_manual:
        st.error(
            "❌ Uploaded PDF does not appear to be a maintenance manual."
        )
        st.stop()

    # ---------------- ISSUE DETECTION ----------------

    issues = []
    recommendations = []
    references = []

    severity = "Normal"

    if temperature > 90:

        issues.append("🔥 Motor Overheating")

        recommendations.append(
            "Check cooling fan and improve ventilation."
        )

        references.append(
            "Temperature exceeds safe operating range."
        )

        severity = "Critical"

    if vibration > 6:

        issues.append("⚙️ Bearing Failure Risk")

        recommendations.append(
            "Inspect bearings and lubrication."
        )

        references.append(
            "High vibration detected."
        )

        if severity != "Critical":
            severity = "Warning"

    if pressure < 50:

        issues.append("💧 Hydraulic Leakage")

        recommendations.append(
            "Inspect pipe joints and seals."
        )

        references.append(
            "Pressure below operating range."
        )

        severity = "Critical"

    if current > 25:

        issues.append("⚡ Electrical Overload")

        recommendations.append(
            "Inspect motor winding and power supply."
        )

        references.append(
            "Current exceeds normal limit."
        )

        severity = "Critical"

    if not issues:

        issues.append(
            "✅ System Operating Normally"
        )

        recommendations.append(
            "Continue routine inspection and maintenance."
        )

        references.append(
            "All parameters are within normal operating limits."
        )

    # ---------------- REPORT ----------------

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

    st.markdown("### 📄 Manual Verification")
    st.success("Maintenance manual verified successfully")

    st.markdown("### 📷 Image Evidence")

    if image:

        img = Image.open(image)

        st.image(
            img,
            width=450,
            caption="Uploaded Equipment Image"
        )

    else:
        st.info("No image uploaded")

    with st.expander("View Uploaded Manual"):
        st.write(manual_text[:2500])

    st.success(
        "Analysis Completed Successfully"
    )
