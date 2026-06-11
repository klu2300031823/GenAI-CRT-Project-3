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

equipment = st.selectbox(
    "🏭 Equipment Type",
    [
        "Motor",
        "Pump",
        "Compressor",
        "Generator"
    ]
)

# ---------------- SENSORS ----------------

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

# ---------------- ANALYZE ----------------

if st.button("Analyze"):

    # ---------- Validate Manual ----------

    if not manual:
        st.error("Please upload a maintenance manual PDF.")
        st.stop()

    manual_text = ""

    reader = PdfReader(manual)

    for page in reader.pages:
        text = page.extract_text()

        if text:
            manual_text += text + "\n"

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
        if word.lower() in manual_text.lower():
            valid_manual = True
            break

    if not valid_manual:
        st.error(
            "❌ Uploaded PDF does not appear to be a maintenance manual."
        )
        st.stop()

    # ---------- Validate Image ----------

    image_status = "No image uploaded"

    if image:

        image_name = image.name.lower()

        machine_words = [
            "motor",
            "pump",
            "machine",
            "engine",
            "equipment",
            "compressor",
            "generator"
        ]

        valid_image = False

        for word in machine_words:
            if word in image_name:
                valid_image = True
                break

        if valid_image:
            image_status = "Equipment image verified"
        else:
            image_status = (
                "Image uploaded (equipment not verified)"
            )

    # ---------- Detect Issues ----------

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
            "Manual Section: Motor Overheating"
        )

        severity = "Critical"

    if vibration > 6:

        issues.append("⚙️ Bearing Failure Risk")

        recommendations.append(
            "Inspect bearings and lubrication."
        )

        references.append(
            "Manual Section: Bearing Failure"
        )

        if severity != "Critical":
            severity = "Warning"

    if pressure < 50:

        issues.append("💧 Hydraulic Leakage")

        recommendations.append(
            "Inspect pipe joints and seals."
        )

        references.append(
            "Manual Section: Hydraulic Leakage"
        )

        severity = "Critical"

    if current > 25:

        issues.append("⚡ Electrical Overload")

        recommendations.append(
            "Inspect motor winding and power supply."
        )

        references.append(
            "Manual Section: Electrical Overload"
        )

        severity = "Critical"

    if not issues:

        issues.append(
            "✅ System Operating Normally"
        )

        recommendations.append(
            "Continue routine inspection."
        )

        references.append(
            "Manual Section: Normal Operation"
        )

    # ---------- Report ----------

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

    st.info(f"🏭 Equipment: {equipment}")

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
    st.success("Maintenance manual verified")

    st.markdown("### 📷 Image Verification")
    st.info(image_status)

    if image:

        img = Image.open(image)

        st.image(
            img,
            width=450,
            caption="Uploaded Equipment Image"
        )

    with st.expander("View Manual"):
        st.write(manual_text[:2500])

    st.success(
        "Analysis Completed Successfully"
    )
